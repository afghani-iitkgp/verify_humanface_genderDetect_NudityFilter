"""

"""
import os
import shutil
import json
from flask import Blueprint
#from flask import request
from werkzeug.utils import secure_filename

import os
from flask import request, render_template, jsonify
#import requests
#import sys
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

from Scripts.Constants import const
from Scripts.Service.aws_s3_image_download import AWS_S3Bucket_download
from Scripts.Service.verify_face import VerifyImage
from Scripts.Service.nudity_filter import NudityFilter
from Scripts.Service.lxapp_image_filtering import LxAppImageFiltering
from Scripts.Service.gender_classification import GenderClassification
from Scripts.Service.gender_detect_v2 import GenderDetectV2
from Scripts.Constants import const

from Scripts.Utility import utils


exception_message = '{"status":False, "status":"Server error, please contact your administrator"}'
method_error_message = '{"status": False, "message": "Method not supported!"}'

x_factor_app_main = Blueprint("XFactorMain", __name__)


@x_factor_app_main.route("/verify_image", methods=["GET", "POST"])
def verify_single_human_face():
    if request.method == "POST":
        try:
            response = dict()


            image_obj_key = request.form["image_link"]
            #
            # # Deleting previously downloaded Images in the local
            # for filename in os.listdir(const.detect_human_face_image_folder):
            #     file_path = os.path.join(const.detect_human_face_image_folder, filename)
            #     try:
            #         if os.path.isfile(file_path) or os.path.islink(file_path):
            #             os.unlink(file_path)
            #         elif os.path.isdir(file_path):
            #             shutil.rmtree(file_path)
            #     except Exception as e:
            #         utils.logger.exception("_deleting all files in the local directory" + str(e))
            #
            #
            #
            #
            #
            # Instantiating the object of class AWS_S3Bucket_download
            aws_conn_obj = AWS_S3Bucket_download()
            # aws_conn_obj.download_single_image_from_s3Bucket(s3_image_key=image_obj_key, dest_folder=const.detect_human_face_image_folder, bucket_name=const.bucket_name)

            img_array = aws_conn_obj.read_image_from_s3(image_obj_key)


            # To walk into the local directory for the image file
            # list_of_image_files = list()
            # for (dirpath, dirnames, filenames) in os.walk(const.detect_human_face_image_folder):
            #     for filename in filenames:
            #         if filename.endswith(tuple(const.image_file_extention)):
            #             list_of_image_files.append(os.sep.join([dirpath, filename]))

            # verify_list_of_image_files = request.files.getlist("images")
            # Instantiating the object of class VerifyImage
            verify_image_obj = VerifyImage()


            result = verify_image_obj.verify_image(image_array=img_array)

            if result == 0:
                response["status"] = 0
                response["message"] = "Unsuccessful, human face is not detected.....Please Try again"

                # return response

            if result == 1:
                response["status"] = 1
                response["message"] = "Successful, human face is detected"



            return response



        except Exception as e:
            utils.logger.exception("--ERROR--> Detecting Human Face" + str(e))
    else:
        return json.dumps(exception_message)



@x_factor_app_main.route("/nudity_filter", methods=["GET", "POST"])
def nudity_check_from_image():
    if request.method == "GET":
        response = dict()

        image_obj_key = request.args.get("image_key")
        #bucket_name = request.args.get("bucketName")

        # # # Deleting previously downloaded Images in the local
        # for filename in os.listdir(const.detect_human_face_image_folder):
        #     file_path = os.path.join(const.detect_human_face_image_folder, filename)
        #     try:
        #         if os.path.isfile(file_path) or os.path.islink(file_path):
        #             os.unlink(file_path)
        #         elif os.path.isdir(file_path):
        #             shutil.rmtree(file_path)
        #     except Exception as e:
        #         utils.logger.exception("_deleting all files in the local directory" + str(e))

        # try:
        #     # Instantiating the object of class AWS_S3Bucket_download
        #     aws_conn_obj = AWS_S3Bucket_download()
        #     aws_conn_obj.download_single_image_from_s3Bucket(s3_image_key=image_obj_key, dest_folder=const.detect_nude_images_folder, bucket_name=const.bucket_name)
        # except Exception as e:
        #     utils.logger.exception("--ERROR--> Downloading from AWS bucket" + str(e))

        try:
            # To walk into the local directory for the image file
            nudity_list_of_image_files = list()
            for (dirpath, dirnames, filenames) in os.walk("./Data/NudeImage"):
                for filename in filenames:
                    if filename.endswith(tuple(const.image_file_extention)):
                        nudity_list_of_image_files.append(os.sep.join([dirpath, filename]))

            # nudity_list_of_image_files = request.files.getlist("images")


            nudity_filter_obj = NudityFilter()

            prediction = nudity_filter_obj.classify_obsence(nudity_list_of_image_files)
            accepted_images = []
            unaccepted_images = []
            threshold = const.nudity_filter_threshold

            for k, v in prediction.items():
                if v["unsafe"] <= threshold:
                    accepted_images.append(k.split("/")[-1])
                if v["unsafe"] > threshold:
                    unaccepted_images.append(k.split("/")[-1])

            data = {}
            #data["prediction"] = prediction
            data["acceptedImageList"] = accepted_images
            data["unacceptedImageList"] = unaccepted_images

            return json.dumps(data)
        except Exception as e:
            utils.logger.exception("--ERROR--> Nudity Filtering check" + str(e))



@x_factor_app_main.route("/detect_gender", methods=["GET", "POST"])
def find_gender_from_image():
    if request.method == "GET":
        response = {}
        # image_obj_key = request.args.get("image_key")

        # # Deleting previously downloaded Images in the local
        # for filename in os.listdir(const.detect_gender_image_folder):
        #     file_path = os.path.join(const.detect_gender_image_folder, filename)
        #     try:
        #         if os.path.isfile(file_path) or os.path.islink(file_path):
        #             os.unlink(file_path)
        #         elif os.path.isdir(file_path):
        #             shutil.rmtree(file_path)
        #     except Exception as e:
        #         utils.logger.exception("_deleting all files in the local directory" + str(e))

        # try:
        #     # Instantiating the object of class AWS_S3Bucket_download
        #     aws_conn_obj = AWS_S3Bucket_download()
        #     aws_conn_obj.download_single_image_from_s3Bucket(s3_image_key=image_obj_key, dest_folder=const.detect_gender_image_folder, bucket_name=const.bucket_name)
        # except Exception as e:
        #     utils.logger.exception("--ERROR--> Downloading from AWS bucket" + str(e))

        try:
            # To walk into the local directory for the image file
            list_of_image_files = list()
            for (dirpath, dirnames, filenames) in os.walk(const.detect_gender_image_folder):
                for filename in filenames:
                    if filename.endswith(tuple(const.image_file_extention)):
                        list_of_image_files.append(os.sep.join([dirpath, filename]))


            gender_dict = {}
            global gender
            for image_obj_key in list_of_image_files:
                find_gender_obj = GenderClassification(img_path=image_obj_key)
                gender = find_gender_obj.find_gender()
                print(gender)
                gender_dict[image_obj_key.split('/')[-1]] = gender
                del find_gender_obj

            response["status"] = 1
            response["gender"] = gender_dict

            return response

        except Exception as e:
            utils.logger.exception("--ERROR--> Detecting Gender from Image" + str(e))




@x_factor_app_main.route("/detect_gender_v2", methods=["GET", "POST"])
def find_gender_from_image_v2():
    if request.method == "POST":
        response = {}

        try:
            # face = request.files['face']
            # image_file = secure_filename(filename=face.filename) # save file to the local disk
            # image_file_path = os.path.join(const.detect_gender_image_folder, image_file)
            # face.save(image_file_path)

            # read image file string data
            filestr = request.files['face'].read()

            # Convert string data to numpy array
            np_img = np.fromstring(filestr, np.uint8)

            # Convert numpy array to image
            image_file = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)


            gender_dict = {}
            gender_detect_obj = GenderDetectV2()
            gender, gender_pred = gender_detect_obj.detect_gender(image_file)

            response["status"] = 1
            response["gender"] = gender
            response["gender_probability"] = list(gender_pred)

            return json.dumps(eval(str(response)))

        except Exception as e:
            utils.logger.exception("--ERROR--> Detecting Gender from Image" + str(e))


@x_factor_app_main.route('/handle_form', methods=['POST'])
def handle_form():
    print("Posted file: {}".format(request.files['file']))
    file = request.files['file']
    files = {'file': file.read()}
    #r = requests.post("http://127.0.0.1:8000/upload/", files=files)


    if type(files['file']) == bytes:
        stream = BytesIO(files['file'])
        image = Image.open(stream).convert("RGB")
        stream.close()
        #image.show()

        lx_app_nudity_filter_obj = LxAppImageFiltering()
        prediction_list = lx_app_nudity_filter_obj.classify_obsence(image)
        accepted_images = []
        unaccepted_images = []
        threshold = const.nudity_filter_threshold


        res = {}
        if prediction_list[0] <= threshold:
            res["isNude"] = 'No'
        else:
            res["isNude"] = 'Yes'


        #return render_template("intex_output.html", results=res)
        return jsonify(res)


        # data = {}
        # # data["prediction"] = prediction
        # data["acceptedImageList"] = accepted_images
        # data["unacceptedImageList"] = unaccepted_images
        #
        # return json.dumps(data)



@x_factor_app_main.route("/upload")
def index():
    print(os.getcwd())
    return render_template("index.html");