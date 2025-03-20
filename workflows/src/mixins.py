from io import BytesIO
from pathlib import Path
import logging
from typing import Optional
from pydantic import BaseModel
from .utils.file import hash_content, write_blob
from .utils.request import fetch
from .settings import BLOB_DIR, STORAGE, PARENT_LOGGER

logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")


class StorageMixin(BaseModel):
    _storage: Path = BLOB_DIR
    blob_name: Optional[str] = None
    content: Optional[bytes] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self._storage.exists():
            logger.info(f"Create directory for storage {self._storage}")
            self._storage.mkdir(parents=True)

    @property
    def filename(self):
        """
        Return the filename
        :return:
        """
        return self.blob_name

    @property
    def fullpath(self):
        """
        Return the storage path of the file
        :return:
        """
        if STORAGE == "s3":
            """"""
        else:
            return Path(self._storage) / self.filename

    async def save(self):
        """
        Save the instance in a blob file
        :return:
        """
        if not self.content:
            raise ValueError(f"Content is empty for {self.__class__}")
        if not self.blob_name:
            self.blob_name = hash_content(self.content)
        await write_blob(BytesIO(self.content), self.fullpath)


class UrlFileMixin(StorageMixin):
    """
    Mixin to download a file from a url
    """

    url: str

    async def retrieve(self):
        """
        Retrieve the image content
        :return:
        """
        logger.info(f"Downloading file {self.url} for {self.__class__}")
        rep = await fetch(url=self.url)
        self.content = rep.content

    async def save(self):
        """
        Save the file
        :return:
        """
        if not self.content and self.url:
            await self.retrieve()
        await super().save()
