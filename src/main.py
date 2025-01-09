from fastapi import FastAPI
from routes.processes import send_command

app = FastAPI()

@app.post("/start")
async def start_feeds():
    response = send_command(f"./Feeds configs.yaml", "start")
    return {"status": response["status"], "pid": response["output"]}

@app.delete("/stop/{pid}")
async def kill_feeds(pid: str):
    response = send_command(pid, "kill")
    return {"status": response["status"], "output": response["output"]}