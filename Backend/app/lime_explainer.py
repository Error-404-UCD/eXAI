from lime import lime_image

class Lime_Explainer:
    def __init__(self, 
                 predict_trained, 
                 predict_untrained, 
                 target_img_width, 
                 target_img_height):
        
        self.predict_trained = predict_trained
        self.predict_untrained = predict_untrained
        self.target_img_height = target_img_height
        self.target_img_width = target_img_width

    def get_lime_explanations(self, test_image, trained=True):

        lime_explainer = lime_image.LimeImageExplainer()

        lime_explanation = ""
        if trained:
            lime_explanation = lime_explainer.explain_instance(test_image[0], 
                                                               self.predict_trained, 
                                                               hide_color=0, 
                                                               num_samples=1000)
        else:
            lime_explanation = lime_explainer.explain_instance(test_image[0], 
                                                               self.predict_untrained, 
                                                               hide_color=0, 
                                                               num_samples=1000)

        temp, mask = lime_explanation.get_image_and_mask(lime_explanation.top_labels[0], 
                                                         positive_only=True, 
                                                         num_features=5, 
                                                         hide_rest=False)
 
        print(f"top label: {lime_explanation.top_labels}")
       
        output = {}
        for key, value in lime_explanation.local_exp.items():
            output[int(key)] = []
            for a, b in value:
                output[int(key)].append({int(a): b})
        
        return {"mask": mask.tolist(), "local_exp": output}
