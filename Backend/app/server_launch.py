from utils.imager import Imager
from utils.numpyarrayencoder import NumpyArrayEncoder
from utils.converter import Converter
import configparser
from flask import Flask, request
from flask_cors import CORS
import os
import json
from data_loader import Data_Loader
from feed_forward_network import FeedForwardNetwork
from shap_explainer import Shap_Explainer
from lime_explainer import Lime_Explainer

if __name__ == "__main__":
    config = configparser.ConfigParser()

    script_dir = "app"
    config_file_path = os.path.join(script_dir, "config.ini")
    config.read(config_file_path)
    config.read(config_file_path)
    print(list(config.keys()))

    # Get configuration constants
    astro_img_folder            = script_dir + "/" + str(config["MLMODEL"]["AstronomyImagesPath"])
    astro_checkpoint_path       = script_dir + "/" + str(config["MLMODEL"]["CheckpointsPath"] +
                                    config["MLMODEL"]["AstronomyModelCheckpointName"])
    mnist_img_folder            = script_dir + "/" + str(config["MLMODEL"]["MNISTImagesPath"])
    mnist_checkpoint_path       = script_dir + "/" + str(config["MLMODEL"]["CheckpointsPath"] +
                                    config["MLMODEL"]["MNISTModelCheckpointName"])
    
    target_img_width            = int(config["MLMODEL"]["TargetImageWidth"])
    target_img_height           = int(config["MLMODEL"]["TargetImageHeight"])
    batch_size                  = int(config["MLMODEL"]["BatchSize"])
    change_target_dim           = int(config["MLMODEL"]["ChangeImageTargetDim"])
    default_dataset             = str(config["MLMODEL"]["DefaultDatasetSelection"])
    epochs                      = int(config["MLMODEL"]["Epochs"])

    ip_address                  = str(config["ROUTING"]["IP"])
    port                        = int(config["ROUTING"]["PORT"])
    
    print(f"mnist_img_folder: {mnist_img_folder}")
    print(f"mnist_checkpoint_path: {mnist_checkpoint_path}")

    
    if change_target_dim == 0:
        target_img_width = -1
        target_img_height = -1

    img_folder = ""
    checkpoint_path = ""

    if default_dataset == "MNIST":
        img_folder = mnist_img_folder
        checkpoint_path = mnist_checkpoint_path
    elif default_dataset == "ASTRO":
        img_folder = astro_img_folder
        checkpoint_path = astro_checkpoint_path

    print(f"Dataset: {default_dataset}")
    print(f"img_folder: {img_folder}")
    print(f"checkpoint_path: {checkpoint_path}")

    data_loader = Data_Loader(
            image_folder=img_folder,
            target_img_width=target_img_width,
            target_img_height=target_img_height,
            batch_size=batch_size)
    
    ffn_super = FeedForwardNetwork(
                                data_loader.target_img_width,
                                data_loader.target_img_height,
                                data_loader.class_names)
    
    ffn_super.train(train_gen=data_loader.train_generator, 
                    val_gen= data_loader.val_generator, 
                    batch_size=batch_size, 
                    checkpoint_path=checkpoint_path,
                    epochs=epochs, 
                    train_count=data_loader.get_train_count(), 
                    val_count=data_loader.get_val_count())
    
    ffn_tiny = FeedForwardNetwork(
                                data_loader.target_img_width,
                                data_loader.target_img_height,
                                data_loader.class_names)
    
    # Train the model to get better results
    # ffn_tiny.train
 
    shap = Shap_Explainer()
    lime = Lime_Explainer()

    app = Flask(__name__)
    CORS(app)
    busy = False
    @app.route('/limeshapexplain/gradient=<gradient>&&background=<bg_count>&&mlModel=<model>', methods=['GET', 'POST'])
    def limeshap_explain(gradient, bg_count, model):
        global busy
        print(f"Req: {len(request.files)}")
        if request.method == 'POST':
            f = request.files['file']
            print(f"Found file: {f}")
            if not busy:
                image = Imager.load_image(f, 
                    (target_img_width,
                    target_img_height))
                
                gradient = Converter.str2bool(gradient)
                bg_count = int(bg_count)
                blackbox = ffn_super if model == "M1" else ffn_tiny
                busy = True
                shapval = shap.get_explanation(blackbox.model, data_loader.get_validation_images(count=bg_count), image)
                limeval = lime.get_explanation(image, predict_fn=blackbox.predict)
                classes = blackbox.get_classes()
                prediction = blackbox.get_prediction(image)
                busy = False
                numpyData = { "shaparray": shapval, "limearray": limeval, "prediction": prediction, "classes": classes }
                encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
    
                return encodedNumpyData
        return None
    
    port = int(os.environ.get('PORT', port))
    app.run(debug=False, host=ip_address, port=port)
