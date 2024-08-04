import shap

class ShapExplainer:
    """
    Provides SHAP explanations for deep learning models.
    """
    def get_explanation(blackbox, background, test_image):
        """
        Generates SHAP explanations for a given test image using the DeepExplainer.
        Parameters
        ----------
        blackbox : FeedForward Network Model
            The trained feedforward network model to explain.
        background : Tensor
            Tensor to use as the background dataset for SHAP.
        test_image : Tensor
            Image for which the explanation is to be generated.
        Returns
        -------
        Array
            SHAP values for the test image.
        """
        e = shap.DeepExplainer(blackbox, background)
        shap_values = e.shap_values(test_image)
        return shap_values