from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/view",StaticFiles(directory="view"))

@app.get("/")
def root():
    return RedirectResponse("/view/index.html")

@app.get("/one")
def step_one():
    return{"step":"one"}

@app.get("/two")
def step_one():
    return{"step":"two"}

@app.get("three")
def step_one():
    return{"step":"three"}