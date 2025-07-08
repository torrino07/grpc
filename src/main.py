import subprocess
from utils import start, stop
from concurrent import futures
import command_pb2
import command_pb2_grpc

import grpc


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
    try:
        pid = start("procstat", "default", '0', '--filters feeds --target 5554')
        print(f"Started procstat@default with PID {pid}")
    except Exception as e:
        print(f"Failed to start procstat@default: {e}")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    command_pb2_grpc.add_CommandExecutorServicer_to_server(CommandExecutorServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("gRPC server started on port 50052")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
