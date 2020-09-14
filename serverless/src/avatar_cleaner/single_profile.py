import aws_utils as aws
import boto3
from custom_logging import configure_logging
from dynaconf import settings

S3 = boto3.client("s3")
LOGGER = configure_logging("acsp")


def lambda_handler(event, context):
    LOGGER.debug("cleaner started")

    LOGGER.debug("(getting event trigger)")
    trigger = aws.S3File.from_event(event)
    LOGGER.info(f"triggered by: {trigger}")

    LOGGER.debug(f"# getting avatars for profile {trigger.subject}")
    avatars = sorted(
        aws.list_bucket(S3, trigger.bucket, trigger.path),
        key=lambda _avatar: _avatar.last_modified,
    )
    if settings.DEBUG:
        LOGGER.debug(f"# listing of avatars")
        for avatar in avatars:
            log = f"*** {avatar.last_modified} *** {avatar.key}"
            LOGGER.debug(log)
        LOGGER.debug(f"end avatars")
    LOGGER.info(f"found {len(avatars)} avatars for profile {trigger.subject}")

    avatars_to_remove = avatars[:-1]
    LOGGER.info(
        f"{len(avatars_to_remove)} avatars to remove for profile {trigger.subject}"
    )

    for avatar in avatars_to_remove:
        LOGGER.debug(f"# removing {avatar}")
        S3.delete_object(Bucket=avatar.bucket, Key=avatar.key)
        LOGGER.debug(f"avatar {avatar} has been removed")

    LOGGER.info(
        f"finished cleanup for profile {trigger.subject} in path {trigger.path}"
    )
