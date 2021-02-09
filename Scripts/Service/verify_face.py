# import numpy as np
import cv2
# import matplotlib.pyplot as plt

from Scripts.Utility import utils


class VerifyImage:
    def verify_image(self, image_array):

        try:
            # Load the image to be tested
            # test_image = cv2.imread(image_path)

            # Converting to grayscale as opencv expects detector takes in input gray scale images
            test_image_gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

            # Since we know that OpenCV loads an image in BGR format so we need to convert it into RBG format to be able to display its true colours. Let us write a small function for that.

            """Haar Cascade files"""
            # Loading the classifier for frontal face
            haar_cascade_face = cv2.CascadeClassifier("Data/haarcascades/haarcascade_frontalface_alt2.xml")

            """Face Detection"""
            faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor=1.2, minNeighbors=5)

            if len(faces_rects) != 1:
                return 0
            elif len(faces_rects) == 1:
                return 1


        except Exception as e:
            utils.logger.exception("__Error occurred while verifying images__" + str(e))


    def convert_to_RGB(self, image):
        try:
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            utils.logger.exception("__Error while conveting image from BGR to RGB" + str(e))