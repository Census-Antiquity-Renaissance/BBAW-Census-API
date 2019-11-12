from pydantic import BaseModel

class DocumentBase(BaseModel):
  alias: str = None
  dimension: str = None
  name: str = None

class Document(DocumentBase):
  id: int

  class Config:
        orm_mode = True