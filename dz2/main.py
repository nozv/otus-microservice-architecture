from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Author": "NozdrovaVS"}

@app.get("/health/")
def read_healthcheck():
    return {"status": "OK"}

