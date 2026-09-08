# uv pip install fastapi uvicorn
# uvicorn main:app --reload
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {"msg":"main page"}

# /items?skip=10&limit=10
@app.get("/items")
def read_name(skip:int, limit:int):
    return {"skip":skip,"limit":limit}

# /items/id/00033A
@app.get("/items/id/{item_id}")
def read_id(item_id:str):
    return {"item_id":item_id}