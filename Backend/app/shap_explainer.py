import shap

class Shap_Explainer:
    def get_shap_explanations(self, blackbox, background, test_image, gradient=False):
        print(f"background: {len(background)}")
        e = ""
        if not gradient:
            e = shap.DeepExplainer(blackbox, background)
        else:
            e = shap.GradientExplainer(blackbox, test_image)
        shap_values = e.shap_values(test_image)
        return shap_values