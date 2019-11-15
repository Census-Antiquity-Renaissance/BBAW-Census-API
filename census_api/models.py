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

class Monument(Base):
    __tablename__ = "cs_monument"
    __table_args__ = {"schema": "census"}

    id = Column(Integer, primary_key=True, index=True)
    fk_father_id = Column(Integer)
    comment = Column(String)
    details = Column(String)
    inventory = Column(String)
    is_main_monument = Column(String)
    label_name = Column(String)
    subdivision = Column(String)
    variant_name = Column(String)
    dimensions = Column(String)

