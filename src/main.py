import locale
import logging
import subprocess
import shlex

from concurrent import futures
import command_pb2
import command_pb2_grpc

import grpc

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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
    write_env_file(instance_name, args, executable)
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

class CommandExecutorServicer(command_pb2_grpc.CommandExecutorServicer):
    def ExecuteCommand(self, request, context):
        args = request.command
        executable = request.executable
        try:
            print("thjcdkcc")
            instance_name = start(args, executable)
            logging.info(f"Started service {executable}@{instance_name}")
            return command_pb2.CommandResponse(status="running", output=instance_name)
        except Exception as e:
            logging.error("Error executing command: %s", str(e))
            return command_pb2.CommandResponse(status="error", output=str(e))


    def KillProcess(self, request, context):
        instance_name = request.command
        executable = request.executable
        try:
            subprocess.run(["sudo", "systemctl", "stop", f"{executable}@{instance_name}"], check=True)
            return command_pb2.CommandResponse(
                status="terminated",
                output=f"Service {executable}@{instance_name} has been stopped"
            )
        except subprocess.CalledProcessError:
            return command_pb2.CommandResponse(
                status="error",
                output=f"Failed to stop service {executable}@{instance_name}"
            )
        except Exception as e:
            return command_pb2.CommandResponse(status="error", output=str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    command_pb2_grpc.add_CommandExecutorServicer_to_server(CommandExecutorServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
