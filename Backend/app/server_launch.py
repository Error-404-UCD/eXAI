from utils.imager import Imager
from utils.numpyarrayencoder import NumpyArrayEncoder
from utils.converter import Converter
import configparser
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import os
import json
from data_generator import Data_Generator
from feed_forward_network import FeedForwardNetwork
from shap_explainer import Shap_Explainer
from lime_explainer import Lime_Explainer
import h5py
print("h5py file location:", h5py.__file__)


if __name__ == "__main__":
    config = configparser.ConfigParser()

    script_dir = "app"
    config_file_path = os.path.join(script_dir, "config.ini")
    config.read(config_file_path)
    config.read(config_file_path)
    print(list(config.keys()))

    astro_img_folder          = script_dir + "/" + str(config["MLMODEL"]["AstronomyImagesPath"])
    astro_checkpoint_path     = script_dir + "/" + str(config["MLMODEL"]["CheckpointsPath"] +
                            config["MLMODEL"]["AstronomyModelCheckpointName"])
    mnist_img_folder          = script_dir + "/" + str(config["MLMODEL"]["MNISTImagesPath"])
    print(f"mnist_img_folder: {mnist_img_folder}")
    mnist_checkpoint_path     = script_dir + "/" + str(config["MLMODEL"]["CheckpointsPath"] +
                            config["MLMODEL"]["MNISTModelCheckpointName"])
    print(f"mnist_checkpoint_path: {mnist_checkpoint_path}")

    target_img_width    = int(config["MLMODEL"]["TargetImageWidth"])
    target_img_height   = int(config["MLMODEL"]["TargetImageHeight"])
    batch_size          = int(config["MLMODEL"]["BatchSize"])
    change_target_dim   = int(config["MLMODEL"]["ChangeImageTargetDim"])
    default_dataset     = str(config["MLMODEL"]["DefaultDatasetSelection"])
    epochs              = int(config["MLMODEL"]["Epoch"])
    bg_count            = int(config["MLMODEL"]["Count"])
    
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

    data = Data_Generator(image_folder=img_folder,
            checkpoint_path=checkpoint_path,
            target_img_width=target_img_width,
            target_img_height=target_img_height,
            batch_size=batch_size)

    ffn = FeedForwardNetwork(data.target_img_height, 
            data.target_img_width, 
            data.class_names,
            checkpoint_path,
            epochs,
            data.train_X,
            data.train_y,
            data.val_X,
            data.val_y,
            batch_size,
            data.get_train_count(),
            data.get_val_count())
    
    bgimgs =  data.get_validation_images(count=bg_count)
    
    shap = Shap_Explainer()

    lime = Lime_Explainer(ffn.predict_trained, 
                ffn.predict_untrained,
                target_img_width,
                target_img_height)

    app = Flask(__name__)

    CORS(app)

    @app.route('/limeshapexplain/gradient=<gradient>&&mlModel=<model>', methods=['GET', 'POST'])
    def limeshap_explain(gradient, model):
        print(f"Req: {len(request.files)}")
        if request.method == 'POST':
            f = request.files['file']
            print(f"Found file: {f}")
            image = Imager.load_image(f, 
                (target_img_width,
                target_img_height))
            
            gradient = Converter.str2bool(gradient)

            trained = True if model == "M1" else False
                
            print(f"trained: {trained}")

            shapval = shap.get_shap_explanations(ffn.model, data.get_validation_images(count=100), image)
            limeval = lime.get_lime_explanations(image)
            prediction = ffn.get_prediction(image, trained=trained)
            numpyData = { "shaparray": shapval, "limearray": limeval, "prediction": prediction}
            encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
    
        return encodedNumpyData
    
    @app.route('/limeexplain', methods=['GET', 'POST'])
    def lime_explain():
        print(f"Req: {len(request.files)}")
        if request.method == 'POST':
            f = request.files['file']
            print(f"Found file: {f}")
            image = Imager.load_image(f,(target_img_width, target_img_height))
            val = lime.get_lime_explanations(image)
            prediction = ffn.get_prediction(image)
            numpyData = { "limearray": val, "prediction": prediction}
            encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)

        return encodedNumpyData
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
