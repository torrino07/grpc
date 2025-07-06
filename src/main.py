import subprocess
import shlex

from concurrent import futures
import command_pb2
import command_pb2_grpc

import grpc

def get_pid(service_name: str) -> str:
    try:
        result = subprocess.run(
            ["systemctl", "show", service_name, "--property=MainPID", "--value"],
            capture_output=True,
            text=True,
            check=True
        )
        pid = result.stdout.strip()
        return pid if pid != "0" else ""
    except subprocess.CalledProcessError:
        return ""

def get_service_name(pid):
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


def write_env_file(executable, instance_name, args):
    env_dir = f"/etc/{executable}"
    env_path = f"{env_dir}/{instance_name}.env"
    subprocess.run(["sudo", "mkdir", "-p", env_dir], check=True)
    content = f"ARGS={args}"
    subprocess.run(
        f"echo {shlex.quote(content)} | sudo tee {env_path} > /dev/null",
        shell=True,
        check=True
    )

def set_cpu_affinity(executable, instance_name, core):
    dropin_dir = f"/etc/systemd/system/{executable}@{instance_name}.service.d"
    subprocess.run(["sudo", "mkdir", "-p", dropin_dir], check=True)
    conf = f"[Service]\nCPUAffinity={core}\n"
    conf_path = f"{dropin_dir}/override.conf"
    subprocess.run(
        f"echo {shlex.quote(conf)} | sudo tee {conf_path} > /dev/null",
        shell=True,
        check=True
    )

def start(executable, instance_name, core, args):
    write_env_file(executable, instance_name, args)
    set_cpu_affinity(executable, instance_name, core)
    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "start", f"{executable}@{instance_name}"], check=True)
    pid = get_pid(f"{executable}@{instance_name}")
    return pid


def stop(pid):
    service_name = get_service_name(pid)
    if service_name:
        subprocess.run(["sudo", "systemctl", "stop", service_name], check=True)
        return True, service_name
    else:
        return False, None

class CommandExecutorServicer(command_pb2_grpc.CommandExecutorServicer):
    def Start(self, request, context):
        executable = request.executable
        name = request.name
        core = request.core
        args = request.command
        try:
            pid = start(executable, name, core, args)
            return command_pb2.CommandResponse(status="running", output=f"Started service {name} with PID {pid}")
        except Exception as e:
            return command_pb2.CommandResponse(status="error", output=str(e))

    def Stop(self, request, context):
        pid = request.pid
        try:
            success, service_name = stop(pid)
            if success:
                return command_pb2.CommandResponse(
                    status="terminated",
                    output=f"Stopped service: {service_name} (PID {pid})"
                )
            else:
                return command_pb2.CommandResponse(
                    status="error",
                    output=f"Could not determine service name for PID {pid}"
                )
        except subprocess.CalledProcessError as e:
            return command_pb2.CommandResponse(
                status="error",
                output=f"Failed to stop service for PID {pid}: {str(e)}"
            )
        except Exception as e:
            return command_pb2.CommandResponse(
                status="error",
                output=str(e)
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    command_pb2_grpc.add_CommandExecutorServicer_to_server(CommandExecutorServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
