from lime import lime_image

class LimeExplainer:
    def get_explanation(test_image, predict_fn):
        lime_explainer = lime_image.LimeImageExplainer()
        # print(predict_fn)
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
