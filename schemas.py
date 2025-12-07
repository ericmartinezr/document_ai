from typing import Optional, List
from pydantic import BaseModel, Field


class DocumentData(BaseModel):
    title: Optional[str] = Field("The title of the document")
    author: Optional[str] = Field("The author of the document")
    publish_date: Optional[str] = Field("The year the document was published")
    summary: Optional[str] = Field("A brief summary of the document")
    # bullet_points: Optional[List[str]] = [Field(
    #    "A list of the most important information in the document")]
