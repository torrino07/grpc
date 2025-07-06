from fastapi import Request, FastAPI
from models import Sockets
from typing import Optional
import json
import grpc
import command_pb2
import command_pb2_grpc
import shlex

app = FastAPI()

def command(
    method: str,
    executable: str,
    name: Optional[str] = None,
    core: Optional[str] = None,
    pid: Optional[str] = None,
    command: Optional[str] = None,
    ):
    with grpc.insecure_channel("[::]:50052") as channel:
        stub = command_pb2_grpc.CommandExecutorStub(channel)
        if method == "start":
            response = stub.Start(command_pb2.StartRequest(
                executable=executable,
                name=name,
                core=core,
                command=command
                ))
        elif method == "stop":
            response = stub.Stop(command_pb2.StopRequest(
                executable=executable,
                pid=pid
                ))
        return {"status": response.status, "output": response.output}
    
@app.post("/api/v1/socket/start")
async def start(request: Request, sockets: Sockets):
    payload = sockets.dict()
    payload_request = json.dumps(payload['request'], separators=(',', ':'))
    target = payload['target']
    args = (
        f"--target {target} "
        f"--host {payload['host']} "
        f"--port {payload['port']} "
        f"--request {payload_request} "
        f"--handshake {payload['handshake']}"
    )
    exchange = payload['exchange']
    market = payload['market']
    core = payload['core']
    executable = "feeds"
    name = f"{exchange}.{market}.{core}.{target}"
    response = command(method="start", executable=executable, name=name, core=core, command=args)
    return {"response": response["output"], "status": response["status"]}


@app.delete("/api/v1/socket/stop/{pid}")
async def stop_etl(request: Request, pid: str):
    executable = "feeds"
    response = command(method="stop", executable=executable, pid=pid)
    return {"response": response["output"], "status": response["status"]}
