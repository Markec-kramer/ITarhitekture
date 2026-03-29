import grpc

import vehicles_pb2
import vehicles_pb2_grpc
from src.logger import get_logger
from src.models import VehicleType
from src.repository import VehicleRepository
from src.service import VehicleService

logger = get_logger(__name__)

_PROTO_TYPE_NAMES = {
    vehicles_pb2.CAR: "CAR",
    vehicles_pb2.VAN: "VAN",
    vehicles_pb2.MOTORCYCLE: "MOTORCYCLE",
}


def _vehicle_to_proto(vehicle) -> vehicles_pb2.Vehicle:
    type_to_proto = {
        VehicleType.CAR: vehicles_pb2.CAR,
        VehicleType.VAN: vehicles_pb2.VAN,
        VehicleType.MOTORCYCLE: vehicles_pb2.MOTORCYCLE,
    }
    return vehicles_pb2.Vehicle(
        id=vehicle.id,
        make=vehicle.make,
        model=vehicle.model,
        type=type_to_proto[vehicle.type],
        year=vehicle.year,
        price_per_day=vehicle.price_per_day,
        available=vehicle.available,
        branch=vehicle.branch,
        license_plate=vehicle.license_plate,
    )


class VehiclesServicer(vehicles_pb2_grpc.VehiclesServiceServicer):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def _make_service(self):
        db = self.session_factory()
        return VehicleService(VehicleRepository(db)), db

    def GetVehicle(self, request, context):
        logger.info(f"gRPC GetVehicle: id={request.id}")
        service, db = self._make_service()
        try:
            vehicle = service.get_vehicle(request.id)
            if not vehicle:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Vehicle {request.id} not found")
                return vehicles_pb2.Vehicle()
            return _vehicle_to_proto(vehicle)
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return vehicles_pb2.Vehicle()
        finally:
            db.close()

    def ListVehicles(self, request, context):
        logger.info(f"gRPC ListVehicles: type_filter={request.type_filter!r}, branch_filter={request.branch_filter!r}")
        service, db = self._make_service()
        try:
            vehicles = service.list_vehicles(
                type_filter=request.type_filter,
                branch_filter=request.branch_filter,
                available_only=request.available_only,
            )
            return vehicles_pb2.ListVehiclesResponse(
                vehicles=[_vehicle_to_proto(v) for v in vehicles]
            )
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return vehicles_pb2.ListVehiclesResponse()
        finally:
            db.close()

    def CreateVehicle(self, request, context):
        logger.info(f"gRPC CreateVehicle: {request.make} {request.model}")
        service, db = self._make_service()
        try:
            vehicle = service.create_vehicle(
                make=request.make,
                model=request.model,
                type=_PROTO_TYPE_NAMES[request.type],
                year=request.year,
                price_per_day=request.price_per_day,
                available=request.available,
                branch=request.branch,
                license_plate=request.license_plate,
            )
            return _vehicle_to_proto(vehicle)
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return vehicles_pb2.Vehicle()
        finally:
            db.close()

    def UpdateVehicle(self, request, context):
        logger.info(f"gRPC UpdateVehicle: id={request.id}")
        service, db = self._make_service()
        try:
            vehicle = service.update_vehicle(
                vehicle_id=request.id,
                make=request.make,
                model=request.model,
                type=_PROTO_TYPE_NAMES[request.type],
                year=request.year,
                price_per_day=request.price_per_day,
                available=request.available,
                branch=request.branch,
                license_plate=request.license_plate,
            )
            if not vehicle:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Vehicle {request.id} not found")
                return vehicles_pb2.Vehicle()
            return _vehicle_to_proto(vehicle)
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return vehicles_pb2.Vehicle()
        finally:
            db.close()

    def DeleteVehicle(self, request, context):
        logger.info(f"gRPC DeleteVehicle: id={request.id}")
        service, db = self._make_service()
        try:
            success = service.delete_vehicle(request.id)
            if not success:
                return vehicles_pb2.DeleteVehicleResponse(
                    success=False,
                    message=f"Vehicle {request.id} not found",
                )
            return vehicles_pb2.DeleteVehicleResponse(success=True, message="Vehicle deleted successfully")
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return vehicles_pb2.DeleteVehicleResponse(success=False, message=str(e))
        finally:
            db.close()
