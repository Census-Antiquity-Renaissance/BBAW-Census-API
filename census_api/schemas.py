from pydantic import BaseModel

class DocumentBase(BaseModel):
  alias: str = None
  dimension: str = None
  name: str = None

class Document(DocumentBase):
  id: int

  class Config:
        orm_mode = True

class MonumentBase(BaseModel):
  comment: str = None
  details: str = None
  is_main_monument: str = None
  label_name: str = None
  subdivision: str = None
  variant_name: str = None
  dimensions: str = None

class Monument(MonumentBase):
  id: int

  class Config:
        orm_mode = True