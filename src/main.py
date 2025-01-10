from fastapi import FastAPI
import grpc
import command_pb2
import command_pb2_grpc
import json
from models import Sockets

app = FastAPI()

host = "0.0.0.0"
port = "50051"

def send_command(command: str, rpc_method: str):
    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = command_pb2_grpc.CommandExecutorStub(channel)
        if rpc_method == "start":
            response = stub.ExecuteCommand(command_pb2.CommandRequest(command=command))
        elif rpc_method == "kill":
            response = stub.KillProcess(command_pb2.CommandRequest(command=command))
        return {"status": response.status, "output": response.output}

@app.post("/api/v1/processes/start")
async def start_feeds(sockets: Sockets):
    args = f"{sockets.host} {sockets.port} '{json.dumps(sockets.request.dict())}' {sockets.handshake} {sockets.topic} {sockets.client} {sockets.clientHost} {sockets.clientPort}"
    response = send_command(f"./Feeds {args}", "start")
    return {"status": response["status"], "pid": response["output"]}

@app.delete("/api/v1/processes/stop/{pid}")
async def kill_feeds(pid: str):
    response = send_command(pid, "kill")
    return {"status": response["status"], "output": response["output"]}