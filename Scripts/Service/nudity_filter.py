import os
import warnings
with warnings.catch_warnings():
    import tensorflow as tf
    import keras
    from keras import backend as K
    import numpy as np
from Scripts.Utility import utils




class NudityFilter:

    def __init__(self):
        """
        url = 'https://github.com/bedapudi6788/NudeNet/releases/download/v0/classifier_model'
        home = os.path.expanduser("~")
        model_folder = os.path.join(home, '.NudeNet/')
        if not os.path.exists(model_folder):
            os.mkdir(model_folder)

        model_path = os.path.join(model_folder, 'classifier')

        if not os.path.exists(model_path):
            print('Downloading the checkpoint to', model_path)
            pydload.dload(url, save_to_path=model_path, max_time=None)
        """
        self.model_path = "./Data/NudityClassifier/classifier_model"

    def load_images(self, image_paths, image_size):
        """
        Function for loading images into numpy arrays for passing to model.predict
        inputs:
            image_paths: list of image paths to load
            image_size: size into which images should be resized

        outputs:
            loaded_images: loaded images on which keras model can run predictions
            loaded_image_indexes: paths of images which the function is able to process
        """
        K.clear_session()

        loaded_images = []
        loaded_image_paths = []

        for i, img_path in enumerate(image_paths):
            try:
                image = keras.preprocessing.image.load_img(img_path, target_size=image_size)
                image = keras.preprocessing.image.img_to_array(image)
                image /= 255
                loaded_images.append(image)
                loaded_image_paths.append(img_path)

            except Exception as ex:
                utils.logger.exception("__ERROR__ while loading image(s) " + str(ex))

        return np.asarray(loaded_images), loaded_image_paths



    def classify_obsence(self, image_paths=[]):
        '''
            inputs:
                image_paths: list of image paths or can be a string too (for single image)
                batch_size: batch_size for running predictions
                image_size: size to which the image needs to be resized
                categories: since the model predicts numbers, categories is the list of actual names of categories
        '''


        """
        When get ----> ValueError: Tensor Tensor("predictions/Softmax:0", shape=(?, 2), dtype=float32) is not an element of this graph.

        K.clear_session() did not work for me

        however, what worked was :
        
        def load_model():
            global model
            model = ResNet50(weights="imagenet")
                    # this is key : save the graph after loading the model
            global graph
            graph = tf.get_default_graph()
        ## While predicting, use the same graph        
            with graph.as_default():
            preds = model.predict(image)
            #... etc
        """
        try:
            #Before prediction
            K.clear_session()


            batch_size = 32
            image_size = (256, 256)

            categories = ["unsafe", "safe"]

            if isinstance(image_paths, str):
                image_paths = list(image_paths)

            loaded_images, loaded_image_paths = self.load_images(image_paths, image_size)

            if not loaded_image_paths:
                return {}

            nsfw_model = keras.models.load_model(self.model_path)
            graph = tf.get_default_graph()
            with graph.as_default():
                model_preds = nsfw_model.predict(loaded_images, batch_size=batch_size)

            preds = np.argsort(model_preds, axis=1).tolist()

            probs = list()
            for i, single_preds in enumerate(preds):
                single_probs = list()
                for j, pred in enumerate(single_preds):
                    single_probs.append(model_preds[i][pred])
                    preds[i][j] = categories[pred]

                probs.append(single_probs)


            images_preds = dict()

            for i, loaded_image_path in enumerate(loaded_image_paths):
                images_preds[loaded_image_path] = dict()
                for j in range(len(preds[i])):
                    images_preds[loaded_image_path][preds[i][j]] = probs[i][j]

            print(images_preds)

            return images_preds

        except Exception as e:
            utils.logger.exception("__ERROR occurred at classification of nude images__" + str(e))

