from fastapi import FastAPI
from app.models import models

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World 2"}