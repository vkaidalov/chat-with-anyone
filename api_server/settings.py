import argparse
import os

import pathlib
from trafaret_config import commandline
from utils import TRAFARET

BASE_DIR = pathlib.Path(__file__).parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'chat_with_anyone.yaml'


def get_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH
    )

    # ignore unknown options
    options, unknown = ap.parse_known_args(argv)

    config = commandline.config_from_options(options, TRAFARET)

    if os.getenv('USE_DOCKER'):
        config['postgres']['host'] = 'chat-database'

    return config
