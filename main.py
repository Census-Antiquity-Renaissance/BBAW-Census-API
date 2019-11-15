from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from census_api import crud, models, schemas
from census_api.database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"msg": "Hello World"}

@app.get("/documents/", response_model=List[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents

@app.get("/document/{document_id}", response_model=schemas.Document)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@app.get("/monuments/", response_model=List[schemas.Monument])
def read_monuments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    monuments = crud.get_monuments(db, skip=skip, limit=limit)
    return monuments

@app.get("/monument/{monument_id}", response_model=schemas.Monument)
def read_monument(monument_id: int, db: Session = Depends(get_db)):
    db_monument = crud.get_monument(db, monument_id=monument_id)
    if db_monument is None:
        raise HTTPException(status_code=404, detail="Monument not found")
    return db_monument

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/people")
async def get_people(name: str = "Edna"):
    return {"name": name.capitalize()}