# Census API

## About

This project connects to a local database containing the Census database (as provided at http://www.census.de/ in 2019 running in easdb4) and creates a very, very basic RESTful API for the Census data.

This project runs on the [FastAPI framework](https://fastapi.tiangolo.com/) for Python 3.

This project has been designed using the steps provided in the [FastAPI documentation for handling relational databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## Prerequisites

This project expects you to have a running postgres database running on your system. Also it expects you already have imported a dump of the Census database.

## git

The main repository resides in:

`git.bbaw.de:/git/census/census_api.git`
https://poetry.eustace.io/
Clone with:

```console
git clone git.bbaw.de:/git/census/census_api.git
```

## Dependencies

* Python 3.7
* Install dependencies using [poetry](https://poetry.eustace.io/)

```console
poetry install
```

## Running

Run project with:

```console
poetry run uvicorn main:app --reload
```

The development server starts and the API can be accessed under: [http://localhost:8000](http://localhost:8000)

## Database Connection

The database connection is currently specified in `census_api/database.py`. This is not good practice and should be externalized using some kind of env-file-system.

```python
# census_api/database.py
SQLALCHEMY_DATABASE_URL = "postgresql://suchmaske@localhost/easydb-census"
```

### Specifying database schema in the model

The FastAPI doesn't specify what to do when you have multiple schemas in your database. In order for the query builder to work correctly, you have to specify the schema in the according model class. The following line is crucial: `__table_args__ = {"schema": "census"}`.

[This thread on StackOverflow](https://stackoverflow.com/questions/27003515/how-to-specify-postgresql-schema-in-sqlalchemy-column-foreign-key-mixin) proved to be very helpful.

```python
# census_api/models.py
class Document(Base):
    __tablename__ = "cs_document"
    __table_args__ = {"schema": "census"}

    id = Column(Integer, primary_key=True, index=True)
    fk_father_id = Column(Integer)
    alias = Column(String)
    dimension = Column(String)
    name = Column(String)
```

## Swagger / OpenAPI

Access the automatically generated [Swagger / OpenAPI](https://swagger.io/) specification at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Further helpful links

* [FastAPI: SQL databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
* [StackOverflow: How to specify PostgreSQL schema in SQLAlchemy column/foreign key mixin?](https://stackoverflow.com/questions/27003515/how-to-specify-postgresql-schema-in-sqlalchemy-column-foreign-key-mixin)

## Tutorial

### Adding the Monuments

1. Take a look a look at the `cs_monument` table in a database explorer tool of your choice. (I like using PyCharm's database explorer.)
2. Determine what columns of that table you want to expose using the API. I have chosen the following:
   1. `id`
   2. `fk_father_id`
   3. `comment`
   4. `details`
   5. `inventory`
   6. `is_main_monument`
   7. `label_name`
   8. `subdivision`
   9. `variant_name`
   10. `dimensions`
3. Create a new class in `models.py` and define those columns:
```python
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
```
1. Now create a class containing the base model for the monuments in `schemas.py` and define all fields you want to expose (for any HTTP request type). The following pattern applies: `field_name: type` or `field_name: type = "default_value"`. Note that `id` is not yet listed. The `BaseModel` covers fields that should always be exposed.
```python
class MonumentBase(BaseModel):
  comment: str = None
  details: str = None
  is_main_monument: str = None
  label_name: str = None
  subdivision: str = None
  variant_name: str = None
  dimensions: str = None
```
5. Next, create a class that extends your `MonumentBase` model. That extended model is used to expose fields you want to use in certain circumstances. For example, the `id` field is only available when fetching data that already exists in the database. Also add a subclass to set the ORM mode. You can find more details about the [Pydantic ORM in FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode) here.
```python
class Monument(MonumentBase):
  id: int

  class Config:
        orm_mode = True
```
6. Now, add the query functions to `crud.py` (CRUD stands for Create, Read, Update, Delete). You can name the functions however you want, however it is a good practice to use the HTTP request type as a prefix. Specify the parameters you need in the query functions. The `db.query()` functions needs the model you want to fetch data from.
```python
def get_monument(db: Session, monument_id: int):
    return db.query(models.Monument).filter(models.Monument.id == monument_id).first()

def get_monuments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Monument).offset(skip).limit(limit).all()
```
7. As a last programming step, specify the routes in `main.py` and add the controller logic. The lines starting with a `@app.get()` are annotations to specify the routes. For example, `@app.get("/monument/{monument_id}", response_model=schemas.Monument)` specifies, that you can get information about monument using a route like `/monument/152707`. The function parameters can help to specify additional query parameters. The function body itself then handles using those parameters, calling the database query and return the data. Also refer to the [appropriate part of the FastAPI documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-your-fastapi-path-operations)
```python
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
```
8. As a final step, run the app from the command line. Make to navigate in the root directory of the project beforehand.
```console
poetry run uvicorn main:app --reload
```
9. Open your browser and visit <http://localhost:8000/monuments> to fetch the first 100 monuments.
10. Open another tab and visit <http://localhost:8000/monument/152707> to fetch a specific monument.

## License

This repository is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

The developers are in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

See http://www.gnu.org/licenses/.

## Credits

© 2018-2020 by Berlin-Brandenburg Academy of Sciences and Humanities

Developed by TELOTA, a DH working group of the Berlin-Brandenburg Academy of Sciences and Humanities http://www.bbaw.de/telota telota@bbaw.de. Developer: Oliver Pohl
