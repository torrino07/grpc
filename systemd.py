import subprocess
import shlex
import psutil
import time


def get_service_name_from_pid(pid):
    try:
        with open(f"/proc/{pid}/cgroup", "r") as f:
            for line in f:
                if "system.slice" in line:
                    parts = line.strip().split("/")
                    for part in parts:
                        if part.endswith(".service"):
                            return part
                elif "name=systemd" in line:
                    parts = line.strip().split("/")
                    for part in parts:
                        if part.endswith(".service"):
                            return part
    except FileNotFoundError:
        return None
    return None


def extract(args: str, key: str = "target") -> str:
    parts = args.strip().split("--")
    values = []
    for part in parts:
        if part:
            items = part.strip().split(maxsplit=1)
            if len(items) > 1:
                values.append(items[1])
            if items[0] == key:
                break
    return ".".join(values), values[-2]

def write_env_file(instance_name, args, executable):
    env_dir = f"/etc/{executable}"
    env_path = f"{env_dir}/{instance_name}.env"
    subprocess.run(["sudo", "mkdir", "-p", env_dir], check=True)
    content = f"ARGS={args}"
    subprocess.run(
        f"echo {shlex.quote(content)} | sudo tee {env_path} > /dev/null",
        shell=True,
        check=True
    )

def set_cpu_affinity(instance_name, core, executable):
    dropin_dir = f"/etc/systemd/system/{executable}@{instance_name}.service.d"
    subprocess.run(["sudo", "mkdir", "-p", dropin_dir], check=True)
    conf = f"[Service]\nCPUAffinity={core}\n"
    conf_path = f"{dropin_dir}/override.conf"
    subprocess.run(
        f"echo {shlex.quote(conf)} | sudo tee {conf_path} > /dev/null",
        shell=True,
        check=True
    )

def start(args, executable):
    instance_name, core = extract(args)
    print(instance_name, core)
    write_env_file(instance_name, args)
    set_cpu_affinity(instance_name, core)
    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "start", f"{executable}@{instance_name}"], check=True)
    return instance_name


def stop(pid):
    service_name = get_service_name_from_pid(pid)
    if service_name:
        subprocess.run(["sudo", "systemctl", "stop", service_name], check=True)
        print(f"✅ Stopped service: {service_name}")
    else:
        print("❌ Could not determine service name from PID.")


def get_process_info():
    process_info = []

    print("🔍 Processes and their CPU affinities:")

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
                uptime_sec = round(time.time() - start_time, 2)
                
                print(f"  - PID {pid} is pinned to cores: {affinity}")

                process_info.append({
                    "args": cmdline,
                    "status": status,
                    "pid": pid,
                    "name": name,
                    "mem_mb": round(mem_mb, 2),
                    "cpu_percent": cpu,
                    "num_threads": num_threads,
                    "affinity": affinity,
                    "start_time": start_time,
                    "uptime_sec": uptime_sec
                })
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

    return process_info

def get_cores(logical=True):
    return psutil.cpu_count(logical=logical)

args='--exchange binance --market spot --type socket --core 1 --target 5559 --host stream.binance.com --port 443 --request {"method":"SUBSCRIBE","params":["btcusdt@depth10@100ms","btcusdt@trade"],"id":1} --handshake /stream?streams='

#start(args)
process_info = get_process_info()
print(process_info)

# stop(2767)