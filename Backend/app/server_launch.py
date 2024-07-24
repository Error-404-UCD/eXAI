from utils.imager import Imager
from utils.numpyarrayencoder import NumpyArrayEncoder
from utils.converter import Converter
import configparser
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import os
import json
from data import Data
#import ffn
from ffn import FFN
from shapy import Shapy
from limey import Limey
from data import Data
import h5py
print("h5py file location:", h5py.__file__)


if __name__ == "__main__":
    config = configparser.ConfigParser()

    # Need to provide absolute path
    # https://stackoverflow.com/questions/77226532/configparser-for-ini-file-throwing-key-error-when-running-using-docker-image-in

    # script_dir = os.path.dirname(os.path.abspath(__file__))
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
    # if change target dim == 0 then set target_img_width, target_img_height = -1
    if change_target_dim == 0:
        target_img_width = -1
        target_img_height = -1

    # change dataset as per selection
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

    # explainer = Explainer(
    #         image_folder=img_folder,
    #         checkpoint_path=checkpoint_path,
    #         target_img_width=target_img_width,
    #         target_img_height=target_img_height,
    #         batch_size=batch_size,
    #         epoch=epoch
    #     )
       
    data = Data(image_folder=img_folder,
            checkpoint_path=checkpoint_path,
            target_img_width=target_img_width,
            target_img_height=target_img_height,
            batch_size=batch_size)
    
    class_names = data.class_names
    train_imgs = data.train_imgs
    val_imgs = data.val_imgs

    ffn = FFN(checkpoint_path=checkpoint_path, 
              target_img_height=data.target_img_height, 
              target_img_width=data.target_img_width, 
              batch_size=batch_size,
              train_imgs=train_imgs,
              val_imgs=val_imgs,
              class_names=class_names,
              epochs=epochs)
    
    bgimgs =  data.get_validation_images(count=bg_count)
    
    shap = Shapy()
    #shap.get_shap_explanation()
    lime = Limey(target_img_height=target_img_height,
                 target_img_width=target_img_width)
    # explainer.explain_lime_random()
    # explainer.explain_shap_random()

    app = Flask(__name__)
    # Use CORS when running server and the client on the same machine
    CORS(app)

    # https://rapidapi.com/guides/upload-files-react-axios
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
            shapval = shap.get_shap_explanation(image, gradient=gradient, trained=trained, count=bg_count)
            limeval = lime.get_lime_explanations(image, predict_trained=ffn.predict_trained, predict_untrained=ffn.predict_untrained)
            prediction = ffn.get_prediction(image, trained=trained)
            # print(limeval)
            # Reference: https://pynative.com/python-serialize-numpy-ndarray-into-json/
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
            # Reference: https://pynative.com/python-serialize-numpy-ndarray-into-json/
            numpyData = { "limearray": val, "prediction": prediction}
            encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)

    
        return encodedNumpyData
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
