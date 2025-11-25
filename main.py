from fastapi import FastAPI
import pyreadstat
import pandas as pd

app = FastAPI()

@app.get("/")
def welcome():
    return {"message": "Bienvenido a la API"}
