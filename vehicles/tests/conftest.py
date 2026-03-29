import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.repository import VehicleRepository
from src.service import VehicleService


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def repository(db_session):
    return VehicleRepository(db_session)


@pytest.fixture
def service(repository):
    return VehicleService(repository)


@pytest.fixture
def sample_vehicle_data():
    return {
        "make": "Toyota",
        "model": "Corolla",
        "type": "CAR",
        "year": 2022,
        "price_per_day": 45.0,
        "available": True,
        "branch": "Ljubljana",
        "license_plate": "LJ-123-AB",
    }
