from lime import lime_image

class Lime_Explainer:
    """
    A class used to provide explanations for image classification predictions using LIME (Local Interpretable Model-agnostic Explanations).

    Methods
    -------
    get_explanation(test_image, predict_fn)
        Generates a LIME explanation for a given image and prediction function.
    """
    def get_explanation(self, test_image, predict_fn):
        """
        Generate a LIME explanation for a given image and prediction function.

        Parameters
        ----------
        test_image : np.array
            The image to be explained, expected to be in the format (height, width, channels).
        predict_fn : function
            The prediction function that takes an image as input and returns class probabilities.

        Returns
        -------
        dict
            A dictionary containing:
            - "mask": A list representing the mask highlighting important features for the prediction.
            - "local_exp": A dictionary mapping class indices to feature importance scores.
        """
        lime_explainer = lime_image.LimeImageExplainer()
        lime_explanation = lime_explainer.explain_instance(test_image[0], 
                                                        predict_fn, 
                                                        hide_color=0, 
                                                        num_samples=1000)
        temp, mask = lime_explanation.get_image_and_mask(lime_explanation.top_labels[0],
                                                        positive_only=False,
                                                        negative_only=False,
                                                        num_features=5)
        output = {}
        for key, value in lime_explanation.local_exp.items():
            output[int(key)] = []
            for a, b in value:
                output[int(key)].append({int(a): b})
        return {"mask": mask.tolist(), "local_exp": output}
