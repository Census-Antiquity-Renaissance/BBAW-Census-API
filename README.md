# Census API

## About

This project connects to a local database containing the Census database and creates a very, very basic RESTful API for the Census data.

This project runs on the [FastAPI framework](https://fastapi.tiangolo.com/) for Python 3.

This project has been designed using the steps provided in the [FastAPI documentation for handling relational databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## Prerequisites

This project expects you to have a running postgres database running on your system. Also it expects you already have imported a dump of the Census database.

## git

The main repository resides in:

`git.bbaw.de:/git/census/census_api.git`

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

Access the automatically generated Swagger / OpenAPI specification at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Further helpful links

* [FastAPI: SQL databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)