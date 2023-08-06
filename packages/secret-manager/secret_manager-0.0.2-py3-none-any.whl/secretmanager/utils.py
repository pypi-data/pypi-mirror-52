import json
import logging
import os

metadata_endpoint = "http://169.254.169.254/latest/dynamic/instance-identity/document"


def get_region():
    if os.environ.get("APP_ENV") not in ['prod', "preprod"]:
        return None

    # for compatibility with python 2 and 3
    try:
        import urllib.request as url_request
    except ImportError:
        import urllib2 as url_request

    metadata = url_request.urlopen(metadata_endpoint).read()
    metadata_json = json.loads(metadata)
    return metadata_json['region']


def get_app_secret_prefix():
    app_name = os.environ.get("APP_NAME")
    app_env = os.environ.get("APP_ENV")
    return app_name + "_" + app_env


def validate_environment_variables():
    app_env = os.environ.get("APP_ENV")
    app_name = os.environ.get("APP_NAME")

    if not app_name:
        raise Exception("application name is not set")

    if not app_env:
        raise Exception("application env is not set")


def get_logger():
    logger = logging.getLogger("secret-manager")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    return logger
