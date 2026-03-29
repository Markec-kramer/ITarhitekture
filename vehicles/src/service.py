from typing import List, Optional

from src.logger import get_logger
from src.models import Vehicle, VehicleType
from src.repository import VehicleRepository

logger = get_logger(__name__)

VALID_TYPES = {vt.value for vt in VehicleType}


class VehicleService:
    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        if vehicle_id <= 0:
            raise ValueError("Vehicle ID must be positive")
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            logger.warning(f"Vehicle id={vehicle_id} not found")
        return vehicle

    def list_vehicles(
        self,
        type_filter: str = "",
        branch_filter: str = "",
        available_only: bool = False,
    ) -> List[Vehicle]:
        if type_filter and type_filter not in VALID_TYPES:
            raise ValueError(f"Invalid vehicle type '{type_filter}'. Valid: {VALID_TYPES}")
        return self.repository.get_all(
            type_filter=type_filter or None,
            branch_filter=branch_filter or None,
            available_only=available_only,
        )

    def create_vehicle(
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
        self._validate_vehicle_fields(make, model, type, year, price_per_day, branch, license_plate)
        logger.info(f"Service: creating vehicle {make} {model}")
        return self.repository.create(make, model, type, year, price_per_day, available, branch, license_plate)

    def update_vehicle(
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
        if vehicle_id <= 0:
            raise ValueError("Vehicle ID must be positive")
        self._validate_vehicle_fields(make, model, type, year, price_per_day, branch, license_plate)
        logger.info(f"Service: updating vehicle id={vehicle_id}")
        return self.repository.update(vehicle_id, make, model, type, year, price_per_day, available, branch, license_plate)

    def delete_vehicle(self, vehicle_id: int) -> bool:
        if vehicle_id <= 0:
            raise ValueError("Vehicle ID must be positive")
        logger.info(f"Service: deleting vehicle id={vehicle_id}")
        return self.repository.delete(vehicle_id)

    def _validate_vehicle_fields(
        self,
        make: str,
        model: str,
        type: str,
        year: int,
        price_per_day: float,
        branch: str,
        license_plate: str,
    ) -> None:
        if not make.strip():
            raise ValueError("Make is required")
        if not model.strip():
            raise ValueError("Model is required")
        if type not in VALID_TYPES:
            raise ValueError(f"Invalid vehicle type '{type}'. Valid: {VALID_TYPES}")
        if not (1900 <= year <= 2100):
            raise ValueError(f"Invalid year: {year}")
        if price_per_day <= 0:
            raise ValueError("Price per day must be positive")
        if not branch.strip():
            raise ValueError("Branch is required")
        if not license_plate.strip():
            raise ValueError("License plate is required")
