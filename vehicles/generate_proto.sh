#!/bin/bash
set -e

echo "Generating gRPC code from proto/vehicles.proto..."
python -m grpc_tools.protoc \
    -I proto \
    --python_out=. \
    --grpc_python_out=. \
    proto/vehicles.proto

echo "Done! Generated: vehicles_pb2.py, vehicles_pb2_grpc.py"
