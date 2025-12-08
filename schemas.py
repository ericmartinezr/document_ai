from typing import Optional, List
from pydantic import BaseModel, Field


class DocumentData(BaseModel):
    title: str = Field("The title of the document")
    author: str = Field("The author of the document")
    publish_date: str = Field("The year the document was published")
    summary: str = Field("A brief summary of the document")
    # bullet_points: Optional[List[str]] = [Field(
    #    "A list of the most important information in the document")]
