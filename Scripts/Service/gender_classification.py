# Import Necessary packages
import os
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2

class GenderClassification:

    def __init__(self, img_path):
        self.image = cv2.imread(img_path)
        self.gender_classification_model = load_model("./Data/models/gender_classification.model")  # Load pre-trained model

    def preprocessing(self):
        #output = np.copy(self.image)
        image = cv2.resize(self.image, (96, 96))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        return image

    def find_gender(self):
        # run inference on input image
        confidence = self.gender_classification_model.predict(self.preprocessing())[0]
        gender_classes = ["male", "female"]
        idx = np.argmax(confidence)
        gender = gender_classes[idx]

        return gender





