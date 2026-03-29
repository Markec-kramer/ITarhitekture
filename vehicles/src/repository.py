from typing import List, Optional

from sqlalchemy.orm import Session

from src.logger import get_logger
from src.models import Vehicle, VehicleType

logger = get_logger(__name__)


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        logger.info(f"Fetching vehicle id={vehicle_id}")
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_all(
        self,
        type_filter: Optional[str] = None,
        branch_filter: Optional[str] = None,
        available_only: bool = False,
    ) -> List[Vehicle]:
        logger.info(
            f"Listing vehicles: type={type_filter}, branch={branch_filter}, available_only={available_only}"
        )
        query = self.db.query(Vehicle)
        if type_filter:
            query = query.filter(Vehicle.type == VehicleType(type_filter))
        if branch_filter:
            query = query.filter(Vehicle.branch == branch_filter)
        if available_only:
            query = query.filter(Vehicle.available.is_(True))
        return query.all()

    def create(
        self,
        make: str,
        model: str,
        type: str,
        year: int,
        price_per_day: float,
        available: bool,
        branch: str,
        license_plate: str,
    ) -> Vehicle:
        logger.info(f"Creating vehicle: {make} {model} ({license_plate})")
        vehicle = Vehicle(
            make=make,
            model=model,
            type=VehicleType(type),
            year=year,
            price_per_day=price_per_day,
            available=available,
            branch=branch,
            license_plate=license_plate,
        )
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        logger.info(f"Vehicle created with id={vehicle.id}")
        return vehicle

    def update(
        self,
        vehicle_id: int,
        make: str,
        model: str,
        type: str,
        year: int,
        price_per_day: float,
        available: bool,
        branch: str,
        license_plate: str,
    ) -> Optional[Vehicle]:
        logger.info(f"Updating vehicle id={vehicle_id}")
        vehicle = self.get_by_id(vehicle_id)
        if not vehicle:
            logger.warning(f"Vehicle id={vehicle_id} not found for update")
            return None
        vehicle.make = make
        vehicle.model = model
        vehicle.type = VehicleType(type)
        vehicle.year = year
        vehicle.price_per_day = price_per_day
        vehicle.available = available
        vehicle.branch = branch
        vehicle.license_plate = license_plate
        self.db.commit()
        self.db.refresh(vehicle)
        logger.info(f"Vehicle id={vehicle_id} updated")
        return vehicle

    def delete(self, vehicle_id: int) -> bool:
        logger.info(f"Deleting vehicle id={vehicle_id}")
        vehicle = self.get_by_id(vehicle_id)
        if not vehicle:
            logger.warning(f"Vehicle id={vehicle_id} not found for deletion")
            return False
        self.db.delete(vehicle)
        self.db.commit()
        logger.info(f"Vehicle id={vehicle_id} deleted")
        return True
