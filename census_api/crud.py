from sqlalchemy.orm import Session

from . import models, schemas

def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()

def get_monument(db: Session, monument_id: int):
    return db.query(models.Monument).filter(models.Monument.id == monument_id).first()

def get_monuments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Monument).offset(skip).limit(limit).all()