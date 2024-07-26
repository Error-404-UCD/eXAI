import shap

class Shap_Explainer:
    # Make sure that background has multiple images and the images are of same dimensions as the model input size and test_img dimensions
    def get_explanation(blackbox, background, test_image, gradient=False):
        e = ""
        if not gradient:
            e = shap.DeepExplainer(blackbox, background)
        else:
            e = shap.GradientExplainer(blackbox, test_image)
        shap_values = e.shap_values(test_image)
        return shap_values