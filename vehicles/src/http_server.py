import os
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.database import SessionLocal, init_db
from src.logger import get_logger
from src.repository import VehicleRepository
from src.service import VehicleService

logger = get_logger(__name__)

app = FastAPI(
    title="Vehicles API",
    description="REST API za upravljanje vozil (avtomobili, kombiji, motorji). gRPC strežnik teče na portu 50051.",
    version="1.0.0",
)


# ---------- helpers ----------

def _get_service():
    db = SessionLocal()
    return VehicleService(VehicleRepository(db)), db


def _to_dict(vehicle: object) -> dict:
    return {
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "type": vehicle.type.value,
        "year": vehicle.year,
        "price_per_day": vehicle.price_per_day,
        "available": vehicle.available,
        "branch": vehicle.branch,
        "license_plate": vehicle.license_plate,
    }


# ---------- schemas ----------

class VehicleCreate(BaseModel):
    make: str
    model: str
    type: str  # CAR | VAN | MOTORCYCLE
    year: int
    price_per_day: float
    available: bool = True
    branch: str
    license_plate: str

    model_config = {"json_schema_extra": {"example": {
        "make": "Toyota", "model": "Corolla", "type": "CAR",
        "year": 2022, "price_per_day": 45.0, "available": True,
        "branch": "Ljubljana", "license_plate": "LJ-123-AB",
    }}}


class VehicleUpdate(BaseModel):
    make: str
    model: str
    type: str
    year: int
    price_per_day: float
    available: bool
    branch: str
    license_plate: str


# ---------- routes ----------

@app.get("/api/vehicles", tags=["Vehicles"], summary="Seznam vozil")
def list_vehicles(
    type: Optional[str] = None,
    branch: Optional[str] = None,
    available_only: bool = False,
):
    service, db = _get_service()
    try:
        vehicles = service.list_vehicles(
            type_filter=type or "",
            branch_filter=branch or "",
            available_only=available_only,
        )
        return [_to_dict(v) for v in vehicles]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@app.get("/api/vehicles/{vehicle_id}", tags=["Vehicles"], summary="Vozilo po ID")
def get_vehicle(vehicle_id: int):
    service, db = _get_service()
    try:
        vehicle = service.get_vehicle(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail=f"Vozilo {vehicle_id} ne obstaja")
        return _to_dict(vehicle)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@app.post("/api/vehicles", tags=["Vehicles"], summary="Dodaj vozilo", status_code=201)
def create_vehicle(data: VehicleCreate):
    service, db = _get_service()
    try:
        vehicle = service.create_vehicle(**data.model_dump())
        logger.info(f"HTTP: vehicle created id={vehicle.id}")
        return _to_dict(vehicle)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@app.put("/api/vehicles/{vehicle_id}", tags=["Vehicles"], summary="Posodobi vozilo")
def update_vehicle(vehicle_id: int, data: VehicleUpdate):
    service, db = _get_service()
    try:
        vehicle = service.update_vehicle(vehicle_id, **data.model_dump())
        if not vehicle:
            raise HTTPException(status_code=404, detail=f"Vozilo {vehicle_id} ne obstaja")
        logger.info(f"HTTP: vehicle updated id={vehicle_id}")
        return _to_dict(vehicle)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@app.delete("/api/vehicles/{vehicle_id}", tags=["Vehicles"], summary="Izbriši vozilo")
def delete_vehicle(vehicle_id: int):
    service, db = _get_service()
    try:
        success = service.delete_vehicle(vehicle_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Vozilo {vehicle_id} ne obstaja")
        logger.info(f"HTTP: vehicle deleted id={vehicle_id}")
        return {"success": True, "message": "Vozilo izbrisano"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


# mount static files last so /docs and /api/* take priority
app.mount("/", StaticFiles(directory="public", html=True), name="static")


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("HTTP_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
