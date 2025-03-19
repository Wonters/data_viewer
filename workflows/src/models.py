import pandas as pd
from pydantic import BaseModel
from typing import Optional, Dict,Any

class Formula(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

class Title(BaseModel):
    text: str
    index: int
class Paragraph(BaseModel):
    title: Title
    text: str


class Table(BaseModel):
    data: Dict[str, Any]
    title: Title

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, title: str):
        """Convertit un DataFrame en modèle Pydantic"""
        return cls(data=df.to_dict(), title=title)

class Image(BaseModel):
    url: str
    content: Optional[bytes]=None
    description: str

class Dataset(BaseModel):
    url: Optional[str] = None
    name: str
    images: list[Image]
    tables: list[Table]
    paragraphs: list[Paragraph]
    formulas: list[Formula]
