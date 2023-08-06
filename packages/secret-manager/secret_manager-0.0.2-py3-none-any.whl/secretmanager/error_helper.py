import logging

logger = logging.getLogger()


def raise_error(e):
    if e.response['Error']['Code'] == 'DecryptionFailureException':
        logger.error(" Secrets Manager can't decrypt the protected secret text using the provided KMS key")
        raise e
    elif e.response['Error']['Code'] == 'InternalServiceErrorException':
        logger.error(" An error occurred on the server side.")
        raise e
    elif e.response['Error']['Code'] == 'InvalidParameterException':
        logger.error("You provided an invalid value for a parameter.")
        raise e
    elif e.response['Error']['Code'] == 'InvalidRequestException':
        logger.error(" You provided a parameter value that is not valid for the current state of the resource.")
        raise e
    elif e.response['Error']['Code'] == 'ResourceNotFoundException':
        logger.error(" We can't find the resource that you asked for.")
        raise e
