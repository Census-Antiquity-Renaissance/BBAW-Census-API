from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"msg": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/people")
async def get_people(name: str = "Edna"):
    return {"name": name.capitalize()}