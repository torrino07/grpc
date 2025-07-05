from fastapi import Request, FastAPI
from models import Sockets
import json
import grpc
import command_pb2
import command_pb2_grpc

app = FastAPI()

def send_command(executable: str, command: str, rpc_method: str):
    with grpc.insecure_channel("[::]:50052") as channel:
        stub = command_pb2_grpc.CommandExecutorStub(channel)
        request = command_pb2.CommandRequest(executable=executable, command=command)
        if rpc_method == "start":
            response = stub.ExecuteCommand(request)
        elif rpc_method == "kill":
            response = stub.KillProcess(request)
        return {"status": response.status, "output": response.output}
    
@app.post("/api/v1/socket/start")
async def start(request: Request, sockets: Sockets):
    payload = sockets.dict()
    payload_request = json.dumps(payload['request'])
    args = (
        f"--exchange {payload['exchange']} "
        f"--market {payload['market']} "
        f"--type {payload['type']} "
        f"--core {payload['core']} "
        f"--target {payload['target']} "
        f"--host {payload['host']} "
        f"--port {payload['port']} "
        f"--request '{payload_request}' "
        f"--handshake {payload['handshake']}"
    )
    response = send_command("feeds", args, "start")
    pid = response["output"]
    status = response["status"]
    return {"pid": pid,"status": status }


@app.delete("/api/v1/socket/stop/{pid}")
async def stop_etl(request: Request, pid: str):
    send_command("./feeds", pid, "kill")
    return {"response": f"ETL with pid {pid} terminated!"}
