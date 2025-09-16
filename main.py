import json
import random
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx
from schemes import *

app = FastAPI(title="Pokemon Trainer API", version="1.0.0")

# Constants
DB_API_BASE_URL = "http://db_api:7000"
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"

# Dependencies
async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client

# Helper functions
async def make_db_api_request(client, method, endpoint, **kwargs):
    response = await client.request(method, f"{DB_API_BASE_URL}{endpoint}", **kwargs)
    return response

async def make_pokeapi_request(client, endpoint):
    response = await client.get(f"{POKEAPI_BASE_URL}{endpoint}")
    return response

# Routes
@app.get("/getTrainer/{trainer_name}", response_model=dict, tags=["trainers"])
async def get_trainer(trainer_name: str, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await make_db_api_request(client, "GET", f"/getTrainer/{trainer_name}")
    
    if response.status_code == 200:
        trainer = TrainerSchema.model_validate(response.json())
        return {"trainer": trainer.model_dump()}
    raise HTTPException(status_code=404, detail="Trainer not found")

@app.post("/capturePokemon/", response_model=dict, tags=["pokemon"])
async def capture_pokemon(data: CapturePokemonSchema, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await make_db_api_request(
        client, 
        "POST", 
        "/capturePokemon/", 
        json=data.model_dump(serialize_as_any=True)
    )
    
    if response.status_code == 200:
        data = response.json()
        pokemon = PokemonSchema.model_validate(data["pokemon"])
        return {"pokemon": pokemon.model_dump()}
    raise HTTPException(status_code=404, detail="Location not found")

@app.get("/randomLocation/", response_model=dict, tags=["locations"])
async def get_random_location(client: httpx.AsyncClient = Depends(get_http_client)):
    location_id = random.randint(1, 10)
    response = await make_pokeapi_request(client, f"/location/{location_id}")
    
    if response.status_code == 200:
        loc = Location.model_validate(response.json())
        return {"location": loc.model_dump()}
    raise HTTPException(status_code=404, detail="Location not found")

@app.patch("/updatePlayerLocation/", response_model=dict, tags=["trainers"])
async def update_player_location(data: UpdatePlayerLocationSchema, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await make_db_api_request(
        client,
        "PATCH",
        "/updatePlayerLocation/",
        json=data.model_dump(serialize_as_any=True)
    )
    
    if response.status_code == 200:
        trainer = TrainerSchema.model_validate(response.json())
        return {"trainer": trainer.model_dump()}
    raise HTTPException(status_code=404, detail="Trainer not found")

@app.get("/getAreaRandomPokemon/{location_name}", response_model=dict, tags=["pokemon"])
async def get_area_random_pokemon(location_name: str, client: httpx.AsyncClient = Depends(get_http_client)):
    area_response = await get_random_area(location_name, client)
    area_data = json.loads(area_response.body.decode())
    area = LocationArea(**area_data)
    
    random_encounter = random.choice(area.pokemon_encounters)
    response = await client.get(random_encounter.pokemon.url)
    
    if response.status_code == 200:
        pokemon_schema = PokemonSchema.model_validate(response.json())
        return {"pokemon": pokemon_schema.model_dump()}
    raise HTTPException(status_code=404, detail="Pokemon not found")

@app.get("/randomArea/{location_name}", response_model=dict, tags=["locations"])
async def get_random_area(location_name: str, client: httpx.AsyncClient = Depends(get_http_client)):
    location_response = await get_location(location_name, client)
    location_data = json.loads(location_response.body.decode())["location"]
    location = Location(**location_data)
    
    random_area = random.choice(location.areas)
    response = await client.get(random_area.url)
    
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=404, detail="Area not found")

@app.get("/location/{location_name}", response_model=dict, tags=["locations"])
async def get_location(location_name: str, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await make_pokeapi_request(client, f"/location/{location_name}")
    
    if response.status_code == 200:
        loc = Location.model_validate(response.json())
        return {"location": loc.model_dump()}
    raise HTTPException(status_code=404, detail="Location not found")

@app.delete("/deleteTrainer/{trainer_name}", tags=["trainers"])
async def delete_trainer(trainer_name: str, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await make_db_api_request(client, "DELETE", f"/deleteTrainer/{trainer_name}")
    return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/listAllTrainers/", tags=["trainers"])
async def list_all_trainers(client: httpx.AsyncClient = Depends(get_http_client)):
    response = await make_db_api_request(client, "GET", "/listAllTrainers/")
    return JSONResponse(content=response.json(), status_code=response.status_code)

@app.post("/createTrainer", tags=["trainers"])
async def create_trainer(trainer: TrainerSchema, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await make_db_api_request(
        client,
        "POST",
        "/createTrainer",
        json=trainer.model_dump()
    )
    return JSONResponse(content=response.json(), status_code=response.status_code)