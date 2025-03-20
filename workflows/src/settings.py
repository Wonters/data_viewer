import os
from pathlib import Path

PARENT_LOGGER = "prefect"
STORAGE = "disk"  # s3
BLOB_DIR = Path("./blobs")
MINIO_ENDPOINT = "minio"
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
BACKEND_HOST = "localhost"
BACKEND_PORT = 8000
