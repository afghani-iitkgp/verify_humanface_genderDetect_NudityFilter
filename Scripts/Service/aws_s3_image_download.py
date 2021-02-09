import os
import shutil
import boto3

from PIL import Image
from io import BytesIO
import numpy as np

from Scripts.Utility import utils
from Scripts.Constants import const

class AWS_S3Bucket_download:

    def __init__(self):
        self.aws_s3_bucket = dict()

        self.aws_s3_bucket["aws_access_id"] = utils.configuration["aws_s3_bucket_connection"]["aws_access_id"]
        self.aws_s3_bucket["aws_secret_access_key"] = utils.configuration['aws_s3_bucket_connection']['aws_secret_access_key']
        self.aws_s3_bucket["bucket_name"] = utils.configuration['aws_s3_bucket_connection']['bucket_name']
        self.aws_s3_bucket["region"] = utils.configuration['aws_s3_bucket_connection']['region']


    def download_single_image_from_s3Bucket(self, s3_image_key, dest_folder, bucket_name):

        s3_client = boto3.client("s3", aws_access_key_id=self.aws_s3_bucket["aws_access_id"], aws_secret_access_key=self.aws_s3_bucket["aws_secret_access_key"])

        dest_file_name = os.path.join(dest_folder, s3_image_key.split("/")[-1])

        try:
            if s3_image_key.split(".")[-1] in (const.image_file_extention):
                s3_client.download_file(bucket_name, s3_image_key, dest_file_name)
        except Exception as e:
            utils.logger.exception("__Error while downloading from S3 Bucket__" + str(e))




    def read_image_from_s3(self, key):
        """Load image file from s3.

        Parameters
        ----------
        bucket: string
            Bucket name
        key : string
            Path in s3

        Returns
        -------
        np array
            Image array
        """
        s3_conn = boto3.resource('s3', aws_access_key_id=self.aws_s3_bucket["aws_access_id"],
                                 aws_secret_access_key=self.aws_s3_bucket["aws_secret_access_key"],
                                 region_name=self.aws_s3_bucket["region"])
        bucket = s3_conn.Bucket(self.aws_s3_bucket["bucket_name"])

        object = bucket.Object(key)
        response = object.get()
        file_stream = response['Body']
        im = Image.open(file_stream)

        return np.array(im)

    def write_image_to_s3(self, img_array, bucket, key, region_name='ap-southeast-1'):
        """Write an image array into S3 bucket

        Parameters
        ----------
        bucket: string
            Bucket name
        key : string
            Path in s3

        Returns
        -------
        None
        """
        s3 = boto3.resource('s3', region_name)
        bucket = s3.Bucket(bucket)
        object = bucket.Object(key)
        file_stream = BytesIO()
        im = Image.fromarray(img_array)
        im.save(file_stream, format='jpeg')
        object.put(Body=file_stream.getvalue())
