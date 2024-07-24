from lime import lime_image
from utils.imager import Imager
import random

class Limey:
    def __init__(self, predict_trained, predict_untrained, target_img_width, target_img_height):
        self.predict_trained = predict_trained
        self.predict_untrained = predict_untrained
        self.target_img_height = target_img_height
        self.target_img_width = target_img_width

    def get_lime_explanations(self, test_image, trained=True):
        # self.build_train_model()
         # Create a LIME explainer
        lime_explainer = lime_image.LimeImageExplainer()
        # Generate LIME explanation
        lime_explanation = ""
        if trained:
            lime_explanation = lime_explainer.explain_instance(test_image[0], self.predict_trained, hide_color=0, num_samples=1000)
        else:
            lime_explanation = lime_explainer.explain_instance(test_image[0], self.predict_untrained, hide_color=0, num_samples=1000)

        # print(f"Lime: {lime_explanation}")
        # Display the explanation
        temp, mask = lime_explanation.get_image_and_mask(lime_explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=False)
        # print(f"test img: {test_image}")
        # print(f"temp: {temp}")
        # print(f"mask: {mask}")
        print(f"top label: {lime_explanation.top_labels}")
       
        # print(f"top label[0]: {lime_explanation.top_labels[0]}")
        # print(f"lime_explanation.local_exp: {lime_explanation.local_exp}")
        # Convert to regular dictionary object
        output = {}
        for key, value in lime_explanation.local_exp.items():
            output[int(key)] = []
            for a, b in value:
                output[int(key)].append({int(a): b})
        
        # print(output)
        # print(df_weights)
        return {"mask": mask.tolist(), "local_exp": output}
