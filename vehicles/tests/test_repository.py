import pytest

from src.models import VehicleType


class TestVehicleRepositoryCreate:
    def test_create_vehicle(self, repository, sample_vehicle_data):
        vehicle = repository.create(**sample_vehicle_data)
        assert vehicle.id is not None
        assert vehicle.make == "Toyota"
        assert vehicle.model == "Corolla"
        assert vehicle.type == VehicleType.CAR
        assert vehicle.year == 2022
        assert vehicle.price_per_day == 45.0
        assert vehicle.available is True
        assert vehicle.branch == "Ljubljana"
        assert vehicle.license_plate == "LJ-123-AB"

    def test_create_assigns_autoincrement_id(self, repository, sample_vehicle_data):
        v1 = repository.create(**sample_vehicle_data)
        data2 = {**sample_vehicle_data, "license_plate": "MB-456-CD"}
        v2 = repository.create(**data2)
        assert v1.id != v2.id

    def test_create_van_type(self, repository, sample_vehicle_data):
        data = {**sample_vehicle_data, "type": "VAN", "license_plate": "MB-456-CD"}
        vehicle = repository.create(**data)
        assert vehicle.type == VehicleType.VAN

    def test_create_motorcycle_type(self, repository, sample_vehicle_data):
        data = {**sample_vehicle_data, "type": "MOTORCYCLE", "license_plate": "CE-789-EF"}
        vehicle = repository.create(**data)
        assert vehicle.type == VehicleType.MOTORCYCLE


class TestVehicleRepositoryGetById:
    def test_get_by_id_returns_vehicle(self, repository, sample_vehicle_data):
        created = repository.create(**sample_vehicle_data)
        fetched = repository.get_by_id(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.license_plate == "LJ-123-AB"

    def test_get_by_id_not_found(self, repository):
        result = repository.get_by_id(9999)
        assert result is None


class TestVehicleRepositoryGetAll:
    def test_get_all_returns_all(self, repository, sample_vehicle_data):
        repository.create(**sample_vehicle_data)
        data2 = {**sample_vehicle_data, "license_plate": "MB-456-CD"}
        repository.create(**data2)
        result = repository.get_all()
        assert len(result) == 2

    def test_get_all_empty(self, repository):
        result = repository.get_all()
        assert result == []

    def test_filter_by_type_car(self, repository, sample_vehicle_data):
        repository.create(**sample_vehicle_data)
        van_data = {**sample_vehicle_data, "type": "VAN", "license_plate": "MB-456-CD"}
        repository.create(**van_data)
        cars = repository.get_all(type_filter="CAR")
        assert len(cars) == 1
        assert cars[0].type == VehicleType.CAR

    def test_filter_by_type_van(self, repository, sample_vehicle_data):
        repository.create(**sample_vehicle_data)
        van_data = {**sample_vehicle_data, "type": "VAN", "license_plate": "MB-456-CD"}
        repository.create(**van_data)
        vans = repository.get_all(type_filter="VAN")
        assert len(vans) == 1
        assert vans[0].type == VehicleType.VAN

    def test_filter_by_branch(self, repository, sample_vehicle_data):
        repository.create(**sample_vehicle_data)
        mb_data = {**sample_vehicle_data, "branch": "Maribor", "license_plate": "MB-456-CD"}
        repository.create(**mb_data)
        result = repository.get_all(branch_filter="Ljubljana")
        assert len(result) == 1
        assert result[0].branch == "Ljubljana"

    def test_filter_available_only(self, repository, sample_vehicle_data):
        repository.create(**sample_vehicle_data)
        unavailable_data = {**sample_vehicle_data, "available": False, "license_plate": "MB-456-CD"}
        repository.create(**unavailable_data)
        result = repository.get_all(available_only=True)
        assert len(result) == 1
        assert result[0].available is True

    def test_combined_filters(self, repository, sample_vehicle_data):
        repository.create(**sample_vehicle_data)
        van_lj = {**sample_vehicle_data, "type": "VAN", "license_plate": "LJ-VAN-01"}
        repository.create(**van_lj)
        car_mb = {**sample_vehicle_data, "branch": "Maribor", "license_plate": "MB-CAR-01"}
        repository.create(**car_mb)
        result = repository.get_all(type_filter="CAR", branch_filter="Ljubljana")
        assert len(result) == 1
        assert result[0].type == VehicleType.CAR
        assert result[0].branch == "Ljubljana"


class TestVehicleRepositoryUpdate:
    def test_update_make_and_price(self, repository, sample_vehicle_data):
        vehicle = repository.create(**sample_vehicle_data)
        updated = repository.update(
            vehicle.id,
            make="Honda",
            model="Civic",
            type="CAR",
            year=2023,
            price_per_day=60.0,
            available=True,
            branch="Ljubljana",
            license_plate="LJ-123-AB",
        )
        assert updated.make == "Honda"
        assert updated.price_per_day == 60.0

    def test_update_availability(self, repository, sample_vehicle_data):
        vehicle = repository.create(**sample_vehicle_data)
        updated = repository.update(
            vehicle.id,
            make="Toyota",
            model="Corolla",
            type="CAR",
            year=2022,
            price_per_day=45.0,
            available=False,
            branch="Ljubljana",
            license_plate="LJ-123-AB",
        )
        assert updated.available is False

    def test_update_nonexistent_returns_none(self, repository):
        result = repository.update(
            9999, "Honda", "Civic", "CAR", 2023, 60.0, True, "Ljubljana", "XX-000-YY"
        )
        assert result is None


class TestVehicleRepositoryDelete:
    def test_delete_existing_vehicle(self, repository, sample_vehicle_data):
        vehicle = repository.create(**sample_vehicle_data)
        success = repository.delete(vehicle.id)
        assert success is True
        assert repository.get_by_id(vehicle.id) is None

    def test_delete_nonexistent_returns_false(self, repository):
        success = repository.delete(9999)
        assert success is False

    def test_delete_reduces_count(self, repository, sample_vehicle_data):
        v1 = repository.create(**sample_vehicle_data)
        data2 = {**sample_vehicle_data, "license_plate": "MB-456-CD"}
        repository.create(**data2)
        repository.delete(v1.id)
        result = repository.get_all()
        assert len(result) == 1
