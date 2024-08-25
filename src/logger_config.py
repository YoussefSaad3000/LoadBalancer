import logging
import logging.config
import os.path

import yaml

file_path = os.path.abspath(__file__)
config_file_path = os.path.join(file_path, "..", "resources", "logging.yml")


def setup_logging(default_path=config_file_path):
    with open(default_path, 'r') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
