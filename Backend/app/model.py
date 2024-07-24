from abc import ABC
import numpy as np

class Model(ABC):
    def build_weak_model(self):
        pass

    def build_train_model(self):
        pass

    def predict_trained(self, imgs):
        return self.model.predict(imgs)
    
    def predict_untrained(self, imgs):
        return self.weak_model.predict(imgs)

    def get_prediction(self, img, trained=True):
        predictions = ""
        if trained:
            predictions = self.predict_trained(img)
        else:
            predictions = self.predict_untrained(img)
        predicted_class = np.argmax(predictions[0])
        return self.class_names[predicted_class]