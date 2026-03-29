"""
Ročni klient za testiranje vehicles gRPC strežnika.
Poženi: PYTHONPATH=. python client_test.py
(strežnik mora teči na localhost:50051)
"""
import grpc
import vehicles_pb2
import vehicles_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = vehicles_pb2_grpc.VehiclesServiceStub(channel)

        print("=== CREATE vozilo 1 ===")
        v1 = stub.CreateVehicle(vehicles_pb2.CreateVehicleRequest(
            make="Toyota", model="Corolla", type=vehicles_pb2.CAR,
            year=2022, price_per_day=45.0, available=True,
            branch="Ljubljana", license_plate="LJ-123-AB",
        ))
        print(f"Ustvarjeno: {v1}")

        print("\n=== CREATE vozilo 2 ===")
        v2 = stub.CreateVehicle(vehicles_pb2.CreateVehicleRequest(
            make="Ford", model="Transit", type=vehicles_pb2.VAN,
            year=2021, price_per_day=80.0, available=True,
            branch="Maribor", license_plate="MB-456-CD",
        ))
        print(f"Ustvarjeno: {v2}")

        print("\n=== LIST vsa vozila ===")
        response = stub.ListVehicles(vehicles_pb2.ListVehiclesRequest())
        for v in response.vehicles:
            print(f"  [{v.id}] {v.make} {v.model} - {v.branch} - {v.price_per_day}€/dan")

        print("\n=== LIST samo CAR ===")
        response = stub.ListVehicles(vehicles_pb2.ListVehiclesRequest(type_filter="CAR"))
        for v in response.vehicles:
            print(f"  [{v.id}] {v.make} {v.model} (type=CAR)")

        print("\n=== GET vozilo po ID ===")
        v = stub.GetVehicle(vehicles_pb2.GetVehicleRequest(id=v1.id))
        print(f"Pridobljeno: {v}")

        print("\n=== UPDATE vozilo ===")
        updated = stub.UpdateVehicle(vehicles_pb2.UpdateVehicleRequest(
            id=v1.id, make="Toyota", model="Corolla", type=vehicles_pb2.CAR,
            year=2022, price_per_day=55.0, available=False,
            branch="Ljubljana", license_plate="LJ-123-AB",
        ))
        print(f"Posodobljeno: available={updated.available}, price={updated.price_per_day}")

        print("\n=== DELETE vozilo ===")
        result = stub.DeleteVehicle(vehicles_pb2.DeleteVehicleRequest(id=v2.id))
        print(f"Izbrisano: success={result.success}, message={result.message!r}")

        print("\n=== LIST po brisanju ===")
        response = stub.ListVehicles(vehicles_pb2.ListVehiclesRequest())
        print(f"Število vozil: {len(response.vehicles)}")


if __name__ == "__main__":
    run()
