from explainer import Explainer
import configparser
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from PIL import Image
import json




if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    # print(config.sections())
    explainer = Explainer(
            image_folder=config["MLMODEL"]["AstronomyImagesPath"],
            checkpoint_path=
                config["MLMODEL"]["CheckpointsPath"]+config["MLMODEL"]["AstronomyModelCheckpointName"],
            target_img_width=config["MLMODEL"]["TargetImageWidth"],
            target_img_height=config["MLMODEL"]["TargetImageHeight"],
            batch_size=config["MLMODEL"]["BatchSize"]
        )
    
    explainer.predict_random()

    app = Flask(__name__)
    CORS(app)

    # https://rapidapi.com/guides/upload-files-react-axios
    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        print(f"Req: {len(request.files)}")
        if request.method == 'POST':
            f = request.files['file']
            print(f"Found file: {f}")

            # with Image.open(f) as image:

            #     img_tensor = transform(image)
            #     img_tensor = torch.div(img_tensor, 255)
            #     # Reference: https://pytorch.org/docs/stable/generated/torch.Tensor.expand.html
            #     # Reference: https://medium.com/@goelpulkit43/deploy-a-pytorch-convolutional-neural-network-via-rest-api-using-flask-40bf0facd65d
            #     img_tensor = img_tensor.expand(1, 1, 28, 28)
            #     # print the converted Torch tensor
            #     # print(img_tensor)

            #     val = get_shap_values(e, img_tensor)

            #     print(val)
            #     # Reference: https://pynative.com/python-serialize-numpy-ndarray-into-json/
            #     numpyData = {"array": val}
            #     encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)

                # Reference: https://pillow.readthedocs.io/en/stable/handbook/concepts.html
                # print(f"Image mode: {im.mode}")

                

        return {"data":"OK"}
    
    app.run()