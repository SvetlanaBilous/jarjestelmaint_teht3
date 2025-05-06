from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel,Field, field_validator
from uuid import uuid4
from datetime import datetime


app = FastAPI(title="Taksimatka-API",
              description="Yksinkertainen API taksimatkojen hallintaan",
              version="1.0.1",
              openapi_url = "/openapi.json")

# Malli taksimatkalle
class TripCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    passenger_count: int
    distance_km: float
    total_price: float

class Trip(TripCreate):
    id: str = Field(default_factory=lambda: str(uuid4()),
                    description="Matkan yksilöllinen ID")

# Muistiin tallennetut matkat (lista Trip-olioista)
trips_db: List[Trip] = []

# Luo uusi matka
@app.post("/trips", response_model=Trip)
def create_trip(trip_data: TripCreate):
    trip = Trip(**trip_data.model_dump())
    trips_db.append(trip)
    return trip

# Hae yksittäinen matka ID:n perusteella
@app.get("/trips/{trip_id}", response_model=Trip)
def get_trip(trip_id: str):
    for trip in trips_db:
        if trip.id == trip_id:
            return trip
    raise HTTPException(status_code=404, detail="Matkaa ei löytynyt")

# Muokkaa olemassa olevaa matkaa
@app.put("/trips/{trip_id}", response_model=Trip)
def update_trip(trip_id: str, updated_data: TripCreate):
    for i, trip in enumerate(trips_db):
        if trip.id == trip_id:
            updated_trip = Trip(id=trip_id, **updated_data.model_dump())
            trips_db[i] = updated_trip
            return updated_trip
    raise HTTPException(status_code=404, detail="Matkaa ei löytynyt")

# Poista matka
@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: str):
    for i, trip in enumerate(trips_db):
        if trip.id == trip_id:
            del trips_db[i]
            return {"message": "Matka poistettu"}
    raise HTTPException(status_code=404, detail="Matkaa ei löytynyt")

# Lista kaikista matkoista
@app.get("/trips", response_model=List[Trip])
def list_trips():
    return trips_db