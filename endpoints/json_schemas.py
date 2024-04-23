from pydantic import BaseModel, Field
from typing import List


class InfoModel(BaseModel):
    colors: str
    range: int


class DataModel(BaseModel):
    id: int
    text: str
    url: str
    tags: List[str]
    info: InfoModel
