import base64
import json

import boto3
from botocore.exceptions import ClientError
from secretmanager.error_helper import raise_error
from secretmanager.utils import get_app_secret_prefix, get_region, get_logger

logger = get_logger()


class SecretManager:
    aws_service_name = "secretsmanager"
    max_results = 100

    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(
            service_name=SecretManager.aws_service_name,
            region_name=get_region()
        )
        self.app_secrets_prefix = get_app_secret_prefix()
        logger.info("App secrets prefix is " + self.app_secrets_prefix)

    def get_secrets(self):
        application_secrets = self.filter_app_secrets()
        secret_configs = {}
        try:
            for secret in application_secrets:
                secret_id = secret['Name']
                secret_value = self.get_secret_with_id(secret_id)
                secret_key = secret_id[len(self.app_secrets_prefix) + 1:]
                if secret_key:
                    secret_configs[secret_key] = json.loads(secret_value)
                else:
                    secret_configs[secret_id] = json.loads(secret_value)
                logger.info("Got secret for " + secret_id)
        except ClientError as e:
            raise_error(e)
            return None
        return secret_configs

    def filter_app_secrets(self):
        application_secrets = []
        next_token = None
        while True:
            if next_token:
                secrets = self.client.list_secrets(
                    MaxResults=SecretManager.max_results,
                    NextToken=next_token)
            else:
                secrets = self.client.list_secrets(
                    MaxResults=SecretManager.max_results)

            for secret in secrets['SecretList']:
                if self.app_secrets_prefix in secret['Name']:
                    application_secrets.append(secret)

            next_token = secrets.get('NextToken')
            if not next_token:
                break
        return application_secrets

    def get_secret_with_id(self, secret_id):
        secret_value_response = self.client.get_secret_value(
            SecretId=secret_id
        )
        if 'SecretString' in secret_value_response:
            secret_value = secret_value_response['SecretString']
        else:
            secret_value = base64.b64decode(secret_value_response['SecretBinary'])

        return secret_value
