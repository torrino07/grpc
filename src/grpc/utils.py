import shlex
import subprocess

def get_pid(service_name):
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