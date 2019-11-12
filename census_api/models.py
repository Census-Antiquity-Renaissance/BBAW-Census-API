from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from census_api.database import Base

class Document(Base):
    __tablename__ = "cs_document"
    __table_args__ = {"schema": "census"}

    id = Column(Integer, primary_key=True, index=True)
    fk_father_id = Column(Integer)
    alias = Column(String)
    dimension = Column(String)
    name = Column(String)