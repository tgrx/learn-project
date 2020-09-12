import logging

import aws_utils as aws
import boto3
from custom_logging import configure_logging
from dynaconf import settings

s3 = boto3.client("s3")

logger = logging.getLogger("avatar_cleaner")


def lambda_handler(event, context):
    configure_logging()
    logger.debug("cleaner started")

    logger.debug("(getting event trigger)")
    trigger = aws.S3File.from_event(event)
    logger.info(f"triggered by: {trigger}")

    logger.debug(f"# getting avatars for profile {trigger.subject}")
    avatars = sorted(
        aws.list_avatars(s3, trigger), key=lambda _avatar: _avatar.last_modified
    )
    if settings.DEBUG:
        logger.debug(f"# listing of avatars")
        for avatar in avatars:
            log = f"*** {avatar.last_modified} *** {avatar.key}"
            logger.debug(log)
        logger.debug(f"end avatars")
    logger.info(f"found {len(avatars)} avatars for profile {trigger.subject}")

    avatars_to_remove = avatars[:-1]
    logger.info(
        f"{len(avatars_to_remove)} avatars to remove for profile {trigger.subject}"
    )

    for avatar in avatars_to_remove:
        logger.debug(f"# removing {avatar}")
        s3.delete_object(
            Bucket=avatar.bucket,
            Key=avatar.key,
        )
        logger.debug(f"avatar {avatar} has been removed")

    logger.info(
        f"finished cleanup for profile {trigger.subject} in path {trigger.path}"
    )
