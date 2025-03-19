import asyncio
import json
import logging
import pandas as pd
import hashlib
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .settings import BLOB_DIR, PARENT_LOGGER
from .mixins import StorageMixin, UrlFileMixin

logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")

class Formula(UrlFileMixin):
    _storage = BLOB_DIR / "formulas"
    url: Optional[str] = None

class Title(BaseModel):
    text: str
    index: int

class Paragraph(StorageMixin):
    _storage = BLOB_DIR / "paragraphs"
    title: Title

class Table(StorageMixin):
    _storage = BLOB_DIR / "tables"
    _df: pd.DataFrame
    content: Dict[str, Any]
    title: Title

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, title: str):
        """Convertit un DataFrame en modèle Pydantic"""
        instance = cls(content=df.to_dict(), title=title)
        instance._df = df
        instance.blob_name = hashlib.sha256(str(instance.content).encode("utf-8")).hexdigest()
        return instance

    @property
    async def filename(self):
        return f"{self.blob_name}.parquet"

    async def save(self):
        self._df.to_parquet(await self.fullpath, engine="fastparquet")
        logger.info(f"Save table in {self.fullpath}")

class Image(UrlFileMixin):
    _storage = BLOB_DIR / "images"
    description: str


class Dataset(StorageMixin):
    _storage = BLOB_DIR / "datasets"
    url: Optional[str] = None
    name: str
    images: list[Image]
    tables: list[Table]
    paragraphs: list[Paragraph]
    formulas: list[Formula]

    def __str__(self):
        return (f"{self.name}: [images ({len(self.images)}), "
                f"tables ({len(self.tables)}), paragraphs ({len(self.paragraphs)}), "
                f"formulas ({len(self.formulas)})]")

    @property
    def filename(self):
        return f"{self.blob_name}.json"

    def model_dump(self,*args, **kwargs) -> dict[str, Any]:
        return {'tables':[table.blob_name for table in self.tables],
                'paragraphs':[{'title':paragraph.title.text,
                               'index':paragraph.title.index,
                               'blob':paragraph.blob_name}
                              for paragraph in self.paragraphs],
                'formulas':[formula.blob_name for formula in self.formulas],
                'images':[img.blob_name for img in self.images]}

    async def save(self):
        items = [*self.tables,*self.paragraphs,*self.formulas,*self.images]
        await asyncio.gather(*[item.save() for item in items], return_exceptions=True)
        self.content = json.dumps(self.model_dump()).encode("utf-8")
        await super().save()
        logger.info(f"Dataset {self.name} saved")


