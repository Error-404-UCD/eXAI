import shap
# from utils.imager import Imager
# import random


# class Shapy:
      
#     # def get_shap_explanation(self, blackbox, count=100, test_image, gradient=False, trained=True):
#     #     # self.build_train_model()
#     #     e = 0
#     #     if not trained:
#     #         blackbox = self.weak_model
#     #     e = shap.DeepExplainer(blackbox, bgimgs)
#     #     e = shap.GradientExplainer(blackbox, test_image)
#     #     shap_values = e.shap_values(test_image)
#     #     # print(f"Shap values:\n{shap_values}")
#     #     return shap_values
    
#     def get_shap_explanation(self, test_image, gradient=False, trained=True, count=100):
#         # self.build_train_model()
#         images = []
#         for i in range(len(self.val_paths)):
#             images.append(Imager.load_image(self.val_paths[i], (self.target_img_width, self.target_img_height)))
#         if count > len(images):
#             count = len(images)
#         print(f"Background images count for SHAP: {count}")
#         background = images[:count]
#         e = 0

#         blackbox = self.model
#         if not trained:
#             blackbox = self.weak_model

#         if not gradient:
#             e = shap.DeepExplainer(blackbox, background)
#         else:
#             e = shap.GradientExplainer(blackbox, test_image)
#         shap_values = e.shap_values(test_image)
#         # print(f"Shap values:\n{shap_values}")
#         return shap_values


class Shapy:
    def get_explanation(self, blackbox, background, test_image, gradient=False):
        print(f"background: {len(background)}")
        e = ""
        if not gradient:
            e = shap.DeepExplainer(blackbox, background)
        else:
            e = shap.GradientExplainer(blackbox, test_image)
        shap_values = e.shap_values(test_image)
        return shap_values