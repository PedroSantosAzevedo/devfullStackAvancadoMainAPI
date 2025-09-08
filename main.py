from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from APIModels.trainer import Trainer
import fastapi.middleware.cors as cors


app = FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/getTrainer/{trainer_name}")
async def get_trainer(trainer_name: str):
    async with httpx.AsyncClient() as client:
        print("Fetching trainer data...")
        response = await client.get(f"http:///127.0.0.1:5000/getTrainer/{trainer_name}")
        if response.status_code == 200:
            data = response.json()
            trainer =  Trainer.model_validate(data)
            return JSONResponse(content={"trainer": trainer.model_dump()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Trainer not found"}, status_code=404)
        

@app.get("/")
def home():
    return JSONResponse(content={"message": "Welcome to my new Basic FastAPI!"})
