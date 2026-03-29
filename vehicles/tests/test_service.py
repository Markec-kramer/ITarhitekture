import pytest
from unittest.mock import MagicMock

from src.models import Vehicle, VehicleType
from src.service import VehicleService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return VehicleService(mock_repo)


@pytest.fixture
def sample_vehicle():
    v = Vehicle()
    v.id = 1
    v.make = "Toyota"
    v.model = "Corolla"
    v.type = VehicleType.CAR
    v.year = 2022
    v.price_per_day = 45.0
    v.available = True
    v.branch = "Ljubljana"
    v.license_plate = "LJ-123-AB"
    return v


class TestGetVehicle:
    def test_returns_vehicle_when_found(self, service, mock_repo, sample_vehicle):
        mock_repo.get_by_id.return_value = sample_vehicle
        result = service.get_vehicle(1)
        assert result == sample_vehicle
        mock_repo.get_by_id.assert_called_once_with(1)

    def test_returns_none_when_not_found(self, service, mock_repo):
        mock_repo.get_by_id.return_value = None
        result = service.get_vehicle(99)
        assert result is None

    def test_raises_on_zero_id(self, service):
        with pytest.raises(ValueError, match="must be positive"):
            service.get_vehicle(0)

    def test_raises_on_negative_id(self, service):
        with pytest.raises(ValueError, match="must be positive"):
            service.get_vehicle(-5)


class TestListVehicles:
    def test_returns_all_vehicles(self, service, mock_repo, sample_vehicle):
        mock_repo.get_all.return_value = [sample_vehicle]
        result = service.list_vehicles()
        assert len(result) == 1
        mock_repo.get_all.assert_called_once_with(
            type_filter=None, branch_filter=None, available_only=False
        )

    def test_filters_by_type(self, service, mock_repo, sample_vehicle):
        mock_repo.get_all.return_value = [sample_vehicle]
        service.list_vehicles(type_filter="CAR")
        mock_repo.get_all.assert_called_once_with(
            type_filter="CAR", branch_filter=None, available_only=False
        )

    def test_filters_by_branch(self, service, mock_repo, sample_vehicle):
        mock_repo.get_all.return_value = [sample_vehicle]
        service.list_vehicles(branch_filter="Ljubljana")
        mock_repo.get_all.assert_called_once_with(
            type_filter=None, branch_filter="Ljubljana", available_only=False
        )

    def test_filters_available_only(self, service, mock_repo):
        mock_repo.get_all.return_value = []
        service.list_vehicles(available_only=True)
        mock_repo.get_all.assert_called_once_with(
            type_filter=None, branch_filter=None, available_only=True
        )

    def test_raises_on_invalid_type(self, service):
        with pytest.raises(ValueError, match="Invalid vehicle type"):
            service.list_vehicles(type_filter="TRUCK")

    def test_empty_string_type_filter_passes(self, service, mock_repo):
        mock_repo.get_all.return_value = []
        service.list_vehicles(type_filter="")
        mock_repo.get_all.assert_called_once_with(
            type_filter=None, branch_filter=None, available_only=False
        )


class TestCreateVehicle:
    def test_creates_vehicle_successfully(self, service, mock_repo, sample_vehicle):
        mock_repo.create.return_value = sample_vehicle
        result = service.create_vehicle(
            "Toyota", "Corolla", "CAR", 2022, 45.0, True, "Ljubljana", "LJ-123-AB"
        )
        assert result == sample_vehicle
        mock_repo.create.assert_called_once()

    def test_raises_on_empty_make(self, service):
        with pytest.raises(ValueError, match="Make is required"):
            service.create_vehicle("", "Corolla", "CAR", 2022, 45.0, True, "Ljubljana", "LJ-123-AB")

    def test_raises_on_whitespace_make(self, service):
        with pytest.raises(ValueError, match="Make is required"):
            service.create_vehicle("   ", "Corolla", "CAR", 2022, 45.0, True, "Ljubljana", "LJ-123-AB")

    def test_raises_on_empty_model(self, service):
        with pytest.raises(ValueError, match="Model is required"):
            service.create_vehicle("Toyota", "", "CAR", 2022, 45.0, True, "Ljubljana", "LJ-123-AB")

    def test_raises_on_invalid_type(self, service):
        with pytest.raises(ValueError, match="Invalid vehicle type"):
            service.create_vehicle("Toyota", "Corolla", "TRUCK", 2022, 45.0, True, "Ljubljana", "LJ-123-AB")

    def test_raises_on_year_too_old(self, service):
        with pytest.raises(ValueError, match="Invalid year"):
            service.create_vehicle("Toyota", "Corolla", "CAR", 1800, 45.0, True, "Ljubljana", "LJ-123-AB")

    def test_raises_on_year_too_new(self, service):
        with pytest.raises(ValueError, match="Invalid year"):
            service.create_vehicle("Toyota", "Corolla", "CAR", 2200, 45.0, True, "Ljubljana", "LJ-123-AB")

    def test_raises_on_zero_price(self, service):
        with pytest.raises(ValueError, match="Price per day must be positive"):
            service.create_vehicle("Toyota", "Corolla", "CAR", 2022, 0, True, "Ljubljana", "LJ-123-AB")

    def test_raises_on_negative_price(self, service):
        with pytest.raises(ValueError, match="Price per day must be positive"):
            service.create_vehicle("Toyota", "Corolla", "CAR", 2022, -10.0, True, "Ljubljana", "LJ-123-AB")

    def test_raises_on_empty_branch(self, service):
        with pytest.raises(ValueError, match="Branch is required"):
            service.create_vehicle("Toyota", "Corolla", "CAR", 2022, 45.0, True, "", "LJ-123-AB")

    def test_raises_on_empty_license_plate(self, service):
        with pytest.raises(ValueError, match="License plate is required"):
            service.create_vehicle("Toyota", "Corolla", "CAR", 2022, 45.0, True, "Ljubljana", "")

    def test_accepts_van_type(self, service, mock_repo, sample_vehicle):
        mock_repo.create.return_value = sample_vehicle
        service.create_vehicle("Ford", "Transit", "VAN", 2021, 80.0, True, "Maribor", "MB-456-CD")
        mock_repo.create.assert_called_once()

    def test_accepts_motorcycle_type(self, service, mock_repo, sample_vehicle):
        mock_repo.create.return_value = sample_vehicle
        service.create_vehicle("Honda", "CBR", "MOTORCYCLE", 2023, 30.0, True, "Celje", "CE-789-EF")
        mock_repo.create.assert_called_once()


class TestUpdateVehicle:
    def test_updates_vehicle_successfully(self, service, mock_repo, sample_vehicle):
        mock_repo.update.return_value = sample_vehicle
        result = service.update_vehicle(
            1, "Honda", "Civic", "CAR", 2023, 50.0, True, "Maribor", "MB-999-ZZ"
        )
        assert result == sample_vehicle

    def test_returns_none_when_not_found(self, service, mock_repo):
        mock_repo.update.return_value = None
        result = service.update_vehicle(
            99, "Honda", "Civic", "CAR", 2023, 50.0, True, "Maribor", "MB-999-ZZ"
        )
        assert result is None

    def test_raises_on_invalid_id(self, service):
        with pytest.raises(ValueError, match="must be positive"):
            service.update_vehicle(0, "Honda", "Civic", "CAR", 2023, 50.0, True, "Maribor", "MB-999-ZZ")

    def test_raises_on_invalid_type(self, service):
        with pytest.raises(ValueError, match="Invalid vehicle type"):
            service.update_vehicle(1, "Honda", "Civic", "INVALID", 2023, 50.0, True, "Maribor", "MB-999-ZZ")

    def test_raises_on_invalid_price(self, service):
        with pytest.raises(ValueError, match="Price per day must be positive"):
            service.update_vehicle(1, "Honda", "Civic", "CAR", 2023, 0.0, True, "Maribor", "MB-999-ZZ")


class TestDeleteVehicle:
    def test_deletes_existing_vehicle(self, service, mock_repo):
        mock_repo.delete.return_value = True
        result = service.delete_vehicle(1)
        assert result is True
        mock_repo.delete.assert_called_once_with(1)

    def test_returns_false_when_not_found(self, service, mock_repo):
        mock_repo.delete.return_value = False
        result = service.delete_vehicle(99)
        assert result is False

    def test_raises_on_invalid_id(self, service):
        with pytest.raises(ValueError, match="must be positive"):
            service.delete_vehicle(0)

    def test_raises_on_negative_id(self, service):
        with pytest.raises(ValueError, match="must be positive"):
            service.delete_vehicle(-1)
