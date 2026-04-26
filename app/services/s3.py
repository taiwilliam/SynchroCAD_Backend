import mimetypes
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from flask import current_app

# Multipart upload: files > 8MB are split into chunks automatically
_TRANSFER_CONFIG = TransferConfig(
    multipart_threshold=8 * 1024 * 1024,
    multipart_chunksize=8 * 1024 * 1024,
)


class S3Service:
    def init_app(self, app):
        app.config.setdefault("AWS_REGION", "ap-east-2")
        app.config.setdefault("AWS_S3_BUCKET", "synchro-cad-files")
        # Create client once — boto3 clients are thread-safe
        app.extensions["s3_client"] = boto3.client(
            "s3",
            region_name=app.config["AWS_REGION"],
            aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
        )
        app.extensions["s3"] = self

    def _client(self):
        return current_app.extensions["s3_client"]

    def upload(self, file_obj, folder: str, filename: str) -> str:
        key = f"{folder}/{filename}"
        bucket = current_app.config["AWS_S3_BUCKET"]
        content_type, _ = mimetypes.guess_type(filename)
        extra = {"ContentType": content_type} if content_type else {}
        try:
            self._client().upload_fileobj(
                file_obj, bucket, key,
                ExtraArgs=extra,
                Config=_TRANSFER_CONFIG,
            )
        except ClientError as e:
            raise RuntimeError(f"S3 upload failed: {e}") from e
        return key

    def delete(self, key: str) -> None:
        bucket = current_app.config["AWS_S3_BUCKET"]
        try:
            self._client().delete_object(Bucket=bucket, Key=key)
        except ClientError as e:
            raise RuntimeError(f"S3 delete failed: {e}") from e

    def url(self, key: str | None) -> str | None:
        if not key:
            return None
        if key.startswith("http"):
            return key
        bucket = current_app.config["AWS_S3_BUCKET"]
        region = current_app.config["AWS_REGION"]
        return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"


s3 = S3Service()
