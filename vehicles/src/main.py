"""
Zagotavlja oba strežnika hkrati:
  - gRPC na portu 50051
  - HTTP (FastAPI) na portu 8000  →  Swagger: http://localhost:8000/docs
"""
import os
import threading

import uvicorn
from dotenv import load_dotenv

from src.database import init_db
from src.logger import get_logger

load_dotenv()
logger = get_logger(__name__)


def _run_grpc() -> None:
    import concurrent.futures

    import grpc
    import vehicles_pb2_grpc

    from src.database import SessionLocal
    from src.servicer import VehiclesServicer

    port = os.getenv("GRPC_PORT", "50051")
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))

    # gRPC reflection — omogoča testiranje z grpcurl
    from grpc_reflection.v1alpha import reflection
    import vehicles_pb2
    service_names = (
        vehicles_pb2.DESCRIPTOR.services_by_name["VehiclesService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    vehicles_pb2_grpc.add_VehiclesServiceServicer_to_server(VehiclesServicer(SessionLocal), server)
    server.add_insecure_port(f"[::]:{port}")
    logger.info(f"gRPC server starting on port {port}")
    server.start()
    server.wait_for_termination()


def main() -> None:
    init_db()

    grpc_thread = threading.Thread(target=_run_grpc, daemon=True)
    grpc_thread.start()

    from src.http_server import app

    http_port = int(os.getenv("HTTP_PORT", "8000"))
    logger.info(f"HTTP server starting on port {http_port}  →  http://localhost:{http_port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=http_port, log_level="warning")


if __name__ == "__main__":
    main()
