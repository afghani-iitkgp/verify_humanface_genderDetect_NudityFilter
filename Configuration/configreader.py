"""
Purpose: Read the configurations from YAML file
"""

import yaml
from Scripts.Utility import utils



def read_configuration(file_name):
    """

    :param file_name:
    :return: all the configuration constants
    """

    with open(file_name, 'r') as f:
        try:
            return yaml.load(stream=f, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            utils.logger.error("Configuration File Read Error " + str(file_name) + "Error" + str(exc))
