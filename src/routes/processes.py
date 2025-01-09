import grpc
import command_pb2
import command_pb2_grpc

host = "127.0.0.1"
port = "50051"

def send_command(command: str, rpc_method: str):
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = command_pb2_grpc.CommandExecutorStub(channel)
        if rpc_method == "start":
            response = stub.ExecuteCommand(command_pb2.CommandRequest(command=command))
        elif rpc_method == "kill":
            response = stub.KillProcess(command_pb2.CommandRequest(command=command))
        return {"status": response.status, "output": response.output}
