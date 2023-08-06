import os

from secretmanager.secret_manager import SecretManager
from secretmanager.utils import get_logger, validate_environment_variables

logger = get_logger()
validate_environment_variables()
app_env = os.environ.get("APP_ENV")
secrets = dict
if app_env in ['prod', "preprod", "secret_test"]:
    secret_manager = SecretManager()
    secrets = secret_manager.get_secrets()
else:
    logger.info("Secrets disbled for this environment")
