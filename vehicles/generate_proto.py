"""Generira gRPC kodo iz proto/vehicles.proto."""
from grpc_tools import protoc

ret = protoc.main([
    "grpc_tools.protoc",
    "-I", "proto",
    "--python_out=.",
    "--grpc_python_out=.",
    "proto/vehicles.proto",
])

if ret == 0:
    print("Uspešno generirano: vehicles_pb2.py, vehicles_pb2_grpc.py")
else:
    print(f"Napaka pri generiranju (exit code {ret})")
    raise SystemExit(ret)
