import enum

from sqlalchemy import Boolean, Column, Enum, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class VehicleType(str, enum.Enum):
    CAR = "CAR"
    VAN = "VAN"
    MOTORCYCLE = "MOTORCYCLE"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    type = Column(Enum(VehicleType), nullable=False)
    year = Column(Integer, nullable=False)
    price_per_day = Column(Float, nullable=False)
    available = Column(Boolean, default=True, nullable=False)
    branch = Column(String(200), nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Vehicle id={self.id} {self.make} {self.model} [{self.license_plate}]>"
