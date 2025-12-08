from pydantic import BaseModel, Field


class DocumentData(BaseModel):
    title: str = Field("The title of the document")
    author: str = Field("The author of the document")
    publish_date: str = Field("The year the document was published")
    summary: str = Field("A brief summary of the document")
