from explainer import Explainer
from utils.imager import Imager
from utils.numpyarrayencoder import NumpyArrayEncoder
import configparser
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import os
import json




if __name__ == "__main__":
    config = configparser.ConfigParser()

    # Need to provide absolute path
    # https://stackoverflow.com/questions/77226532/configparser-for-ini-file-throwing-key-error-when-running-using-docker-image-in

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, 'config.ini')
    config.read(config_file_path)
    print(list(config.keys()))
    img_folder          = script_dir + "/" + str(config["MLMODEL"]["AstronomyImagesPath"])
    checkpoint_path     = script_dir + "/" + str(config["MLMODEL"]["CheckpointsPath"] +
                            config["MLMODEL"]["AstronomyModelCheckpointName"])
    target_img_width    = int(config["MLMODEL"]["TargetImageWidth"])
    target_img_height   = int(config["MLMODEL"]["TargetImageHeight"])
    batch_size          = int(config["MLMODEL"]["BatchSize"])

    explainer = Explainer(
            image_folder=img_folder,
            checkpoint_path=checkpoint_path,
            target_img_width=target_img_width,
            target_img_height=target_img_height,
            batch_size=batch_size
        )
    
    explainer.explain_lime_random()
    explainer.explain_shap_random()

    app = Flask(__name__)
    CORS(app)

    # https://rapidapi.com/guides/upload-files-react-axios
    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        print(f"Req: {len(request.files)}")
        if request.method == 'POST':
            f = request.files['file']
            print(f"Found file: {f}")
            image = Imager.load_image(f, 
                (target_img_width,
                target_img_height))
            val = explainer.get_shap_explanation(image)
            # Reference: https://pynative.com/python-serialize-numpy-ndarray-into-json/
            numpyData = {"array": val}
            encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)

    
        return encodedNumpyData
    
    app.run()