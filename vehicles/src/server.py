import concurrent.futures
import os

import grpc
import vehicles_pb2_grpc
from dotenv import load_dotenv

from src.database import SessionLocal, init_db
from src.logger import get_logger
from src.servicer import VehiclesServicer

load_dotenv()
logger = get_logger(__name__)


def serve() -> None:
    init_db()

    port = os.getenv("GRPC_PORT", "50051")
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))

    servicer = VehiclesServicer(SessionLocal)
    vehicles_pb2_grpc.add_VehiclesServiceServicer_to_server(servicer, server)

    server.add_insecure_port(f"[::]:{port}")
    logger.info(f"Vehicles gRPC server starting on port {port}")
    server.start()
    logger.info("Server ready. Waiting for requests...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
