import time
from typing import List, Dict

import psutil
import zmq


class ProcessTracker:
    def __init__(self):
        self.processes: List[Dict] = []

    def update(self):
        self.processes.clear()
        for proc in psutil.process_iter(["pid", "name", "cmdline", "create_time", "status"]):
            if "feeds" in proc.info["name"]:
                try:
                    p = psutil.Process(proc.pid)
                    affinity = p.cpu_affinity() if hasattr(p, "cpu_affinity") else "N/A"
                    cmdline = proc.info["cmdline"]
                    name = p.name()
                    pid = p.pid
                    mem_mb = p.memory_info().rss / 1024 / 1024
                    cpu = p.cpu_percent(interval=0.1)
                    status =  proc.info["status"]
                    num_threads = p.num_threads()
                    start_time = proc.info["create_time"]
                    duration = round(time.time() - start_time, 2)
        
                    self.processes.append({
                        "type": "feeds",
                        "args": cmdline,
                        "pid": pid,
                        "cpu": cpu,
                        "mem_mb": round(mem_mb, 2),
                        "num_threads": num_threads,
                        "cores": affinity,
                        "status": status,
                        "name": name,
                        "start_time": start_time,
                        "duration": duration
                    })
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    continue

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5554")
    tracker = ProcessTracker()
    while True:
        tracker.update()
        try:
            socket.send_json(tracker.processes, flags=zmq.NOBLOCK)
        except zmq.Again:
            print("No receiver ready, skipping send")
        time.sleep(1)
