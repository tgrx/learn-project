from datetime import datetime
from typing import Dict
from typing import Generator
from typing import NamedTuple
from typing import Optional

import delorean


class S3File(NamedTuple):
    bucket: str
    key: str
    last_modified: datetime
    location: str
    package: str
    subject: str
    filename: str

    @property
    def path(self) -> str:
        return "/".join((self.location, self.package, self.subject))

    @classmethod
    def from_event(cls, event: Dict) -> "S3File":
        records = event["Records"]
        record = records[0]

        last_modified = delorean.parse(record["eventTime"]).datetime
        s3event = record["s3"]

        bucket = s3event["bucket"]["name"]
        key = s3event["object"]["key"]

        try:
            (location, package, subject, filename) = key.split("/")
        except ValueError as err:
            log = (
                f"Unsupported format of key `{key}`."
                f" Key MUST be in format: location/package/subject/filename."
            )
            raise TypeError(log) from err

        return S3File(
            bucket=bucket,
            filename=filename,
            key=key,
            last_modified=last_modified,
            location=location,
            package=package,
            subject=subject,
        )

    @classmethod
    def from_contents_item(cls, bucket: str, item: Dict) -> "S3File":
        key = item["Key"]
        last_modified = item["LastModified"]
        (location, package, subject, filename) = key.split("/")

        return S3File(
            bucket=bucket,
            filename=filename,
            key=key,
            last_modified=last_modified,
            location=location,
            package=package,
            subject=subject,
        )


def list_bucket(
    s3, bucket: str, path: Optional[str] = None
) -> Generator[S3File, None, None]:
    kwargs = {"Bucket": bucket}
    if path:
        kwargs["Prefix"] = path

    response = s3.list_objects(**kwargs)
    contents = response.get("Contents", [])
    files = (S3File.from_contents_item(bucket=bucket, item=item) for item in contents)
    yield from files
