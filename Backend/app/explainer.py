from abc import ABC

class Explainer(ABC):

    def get_shap_explanation(self, blackbox, background, test_image, gradient=False, trained=True):
        pass

    def get_lime_explanations(self, test_image, trained=True):
        pass
    

