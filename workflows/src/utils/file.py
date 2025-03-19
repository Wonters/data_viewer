import hashlib
import logging
from io import BytesIO
from typing import Union
import aioboto3
import aiofiles
from pathlib import Path
from ..settings import (
    BLOB_DIR,
    AWS_S3_ENDPOINT_URL,
    AWS_SECRET_ACCESS_KEY,
    AWS_ACCESS_KEY_ID,
    AWS_STORAGE_BUCKET_NAME,
    PARENT_LOGGER,
    STORAGE,
)

logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")

def chunk_string_generator(s, chunk_size=4096):
    """Générateur qui renvoie des morceaux de chunk_size caractères"""
    for i in range(0, len(s), chunk_size):
        yield s[i:i + chunk_size]

def hash_content(content):
    hasher = hashlib.sha256()
    for chunk in chunk_string_generator(content, 4096):
        hasher.update(chunk)
    return hasher.hexdigest()

def hash_file(file_path):
    """Calcule le hash SHA-256 d'un fichier."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


async def save_in_s3(content: BytesIO, blob_name: str):
    """
    Store in s3 or Minio container
    :return:
    """
    session = aioboto3.Session()
    async with session.client(
        "s3",
        endpoint_url=AWS_S3_ENDPOINT_URL,  # Spécifique à MinIO
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    ) as s3_client:
        try:
            filepath = ""
            s3_client.upload_content(filepath, AWS_STORAGE_BUCKET_NAME, blob_name)
            logger.info(f"✅ File {filepath.name} uploaded")
        except Exception as e:
            raise e


async def write_blob(content: BytesIO,filepath:Path, storage: str = STORAGE):
    """Store file with a unique hash."""
    if storage == "s3":
        await save_in_s3(content, filepath.name)
    else:
        async with aiofiles.open(filepath, "wb") as blob_file:
            await blob_file.write(content.read())
            logger.info(f"✅ File {filepath} save on disk")
