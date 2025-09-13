import json
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from schemes import *

app = FastAPI()

@app.get("/getTrainer/{trainer_name}")
async def get_trainer(trainer_name: str):
    async with httpx.AsyncClient() as client:
        print("Fetching trainer data...")
        response = await client.get(f"http://db_api:7000/getTrainer/{trainer_name}")
        if response.status_code == 200:
            data = response.json()
            trainer =  TrainerSchema.model_validate(data)
            return JSONResponse(content={"trainer": trainer.model_dump()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Trainer not found"}, status_code=404)
        
@app.post("/capturePokemon/")
async def capture_pokemon(data: CapturePokemonSchema):
    print("Capturing Pokemon...")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://db_api:7000/capturePokemon/", json=data.model_dump(serialize_as_any=True))
        if response.status_code == 200:
            data = response.json()
            pokemon =  PokemonSchema.model_validate(data["pokemon"])
            return JSONResponse(content={"pokemon": pokemon.model_dump()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)      

@app.get("/randomLocation/")
async def get_random_location():
    location = random.randint(1,10)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/location/{location}")
        if response.status_code == 200:
            data = response.json()
            loc =  Location.model_validate(data)
            return JSONResponse(content={"location": loc.model_dump()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)

@app.patch("/updatePlayerLocation/")
async def update_player_location(data: UpdatePlayerLocationSchema):
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            "http://db_api:7000/updatePlayerLocation/",
            json=data.model_dump(serialize_as_any=True)
        )
        print(response.json())
        if response.status_code == 200:
            data = response.json()
            trainer = TrainerSchema.model_validate(data)
            return JSONResponse(content={"trainer": trainer.model_dump()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Trainer not found"}, status_code=404)

@app.get("/getAreaRandomPokemon/{location_name}")
async def get_area_random_pokemon(location_name: str):
    async with httpx.AsyncClient() as client:
        area_response = await get_random_area(location_name)
        area_data = area_response.body.decode()
        area = LocationArea(**json.loads(area_data))
        randomEncounter = area.pokemon_encounters[random.randint(0, len(area.pokemon_encounters)-1)]
        response = await client.get(randomEncounter.pokemon.url)
        if response.status_code == 200:
            pokemonSchema = PokemonSchema.model_validate(response.json())
            return JSONResponse(content={"pokemon": pokemonSchema.model_dump()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)

@app.get("/randomArea/{location_name}")
async def get_random_area(location_name: str):
    async with httpx.AsyncClient() as client:
        location_response = await get_location(location_name)
        location_data = location_response.body.decode()
        
        location_dict = json.loads(location_data)["location"]
        location = Location(**location_dict)
        random_area = location.areas[random.randint(0, len(location.areas)-1)]
        response = await client.get(random_area.url)
        if response.status_code == 200:
            data = response.json()
            return JSONResponse(content=data)
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)

@app.get("/location/{locationName}")
async def get_location(locationName: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/location/{locationName}")
        if response.status_code == 200:
            data = response.json()
            loc =  Location(**data)
            return JSONResponse(content={"location": loc.model_dump()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)
        
@app.delete("/deleteTrainer/{trainer_name}")
async def delete_trainer(trainer_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"http://db_api:7000/deleteTrainer/{trainer_name}")
        return JSONResponse(content=response.json(), status_code=response.status_code)
    
@app.get("/listAllTrainers/")
async def list_all_trainers():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://db_api:7000/listAllTrainers/")
        return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/")
def home():
    return JSONResponse(content={"message": "Welcome to my new Basic FastAPI!"})
