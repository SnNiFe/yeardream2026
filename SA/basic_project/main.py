from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/view",StaticFiles(directory="view"))

@app.get("/")
def root():
    return RedirectResponse("/view/index.html")