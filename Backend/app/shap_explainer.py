import shap

class ShapExplainer:
    # Make sure that background has multiple images and the images are of same dimensions as the model input size and test_img dimensions
    def get_explanation(blackbox, background, test_image):
        e = shap.DeepExplainer(blackbox, background)
        shap_values = e.shap_values(test_image)
        return shap_values