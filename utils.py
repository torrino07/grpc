import grpc
import command_pb2
import command_pb2_grpc

def send_command(executable: str, command: str, rpc_method: str):
    with grpc.insecure_channel("[::]:50052") as channel:
        stub = command_pb2_grpc.CommandExecutorStub(channel)
        request = command_pb2.CommandRequest(executable=executable, command=command)
        if rpc_method == "start":
            response = stub.ExecuteCommand(request)
        elif rpc_method == "kill":
            response = stub.KillProcess(request)
        return {"status": response.status, "output": response.output}