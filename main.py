from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message": "Welcome to the Basic Flask API!"})

@app.get("/ping")
def ping():
    return JSONResponse(content={"response": "pong"})
