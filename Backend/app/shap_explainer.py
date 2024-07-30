import shap

class Shap_Explainer:
    """
    A class used to provide explanations for model predictions using SHAP (SHapley Additive exPlanations).

    Methods
    -------
    get_explanation(blackbox, background, test_image, gradient=False)
        Generates SHAP values for a given image and model using either DeepExplainer or GradientExplainer.
    """
    def get_explanation(self, blackbox, background, test_image, gradient=False):
        """
        Generate SHAP values for a given image and model.

        Parameters
        ----------
        blackbox : tf.keras.Model or callable
            The model or function used for generating predictions.
        background : np.array
            Background dataset used for the SHAP explanation, typically a set of representative examples.
        test_image : np.array
            The image for which the SHAP values are computed.
        gradient : bool, optional
            If True, uses GradientExplainer; otherwise, uses DeepExplainer. Default is False.

        Returns
        -------
        list
            The SHAP values for the provided image.
        """
        e = ""
        if not gradient:
            e = shap.DeepExplainer(blackbox, background)
        else:
            e = shap.GradientExplainer(blackbox, test_image)
        shap_values = e.shap_values(test_image)
        return shap_values