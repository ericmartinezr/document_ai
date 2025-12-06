from pydantic import BaseModel, Field


class DocumentData(BaseModel):
    name: str | None = Field("The name in the document")
    phone: str | None = Field("The phone in the document")
