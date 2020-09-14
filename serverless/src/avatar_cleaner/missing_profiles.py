from typing import Dict
from typing import Generator

import aws_utils
import boto3
from api_utils import call_api
from api_utils import TransformationError
from custom_logging import configure_logging
from dynaconf import settings

LOGGER = configure_logging("acmp")

API = settings.get("API")
assert API, f"no API provided"
LOGGER.debug(f"using API: {API}")

API_TOKEN = settings.get("API_TOKEN")
assert API_TOKEN, f"no API_TOKEN provided"
LOGGER.debug(f"using API_TOKEN: {API_TOKEN[:2]}..{API_TOKEN[-2:]}")

BUCKET = settings.get("BUCKET")
assert BUCKET, f"no BUCKET provided"
LOGGER.debug(f"using BUCKET: {BUCKET}")

LOCATION = settings.get("LOCATION", "")
assert LOCATION, f"no LOCATION provided"
LOGGER.debug(f"using LOCATION: {LOCATION}")

S3 = boto3.client("s3")


def lambda_handler(event: Dict, context):
    LOGGER.debug("# starting cleanup for missing profiles")

    LOGGER.debug(f"# collecting files from bucket: {BUCKET}")
    files = aws_utils.list_bucket(S3, BUCKET, LOCATION)

    LOGGER.debug(f"# collecting avatars")
    avatars = ((item.subject, item) for item in files)

    LOGGER.debug(f"# collecting profiles from api: {API}")
    profiles = frozenset(list_profiles())
    nr_profiles = len(profiles)
    LOGGER.debug(f"api returned {nr_profiles} profile{'s' if nr_profiles > 1 else ''}")

    LOGGER.debug(f"# collecting waste avatars")
    waste_avatars = (avatar for (profile, avatar) in avatars if profile not in profiles)

    nr_avatars = 0
    for nr_avatars, avatar in enumerate(waste_avatars):
        LOGGER.debug(f"*** deleting waste avatar: {avatar.key}")
        S3.delete_object(Bucket=avatar.bucket, Key=avatar.key)

    log = f"{nr_avatars} waste avatars have been deleted from {BUCKET}:{LOCATION}"
    LOGGER.info(log)


def list_profiles() -> Generator[int, None, None]:
    def item_to_profile(position: int, item: Dict) -> str:
        if "profile" not in item:
            raise TransformationError(position, item, "no 'profile' in item")
        profile = item["profile"]
        if not profile:
            raise TransformationError(
                position, item, f"malformed profile `{profile!r}`: empty"
            )
        return str(profile)

    headers = {"AUTHORIZATION": f"Token {API_TOKEN}"}
    profiles = call_api(API, headers=headers, transform=item_to_profile, logger=LOGGER)
    yield from profiles
