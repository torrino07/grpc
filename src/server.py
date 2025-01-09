from concurrent import futures
import grpc
import subprocess
import os
import signal
import command_pb2
import command_pb2_grpc

class CommandExecutorServicer(command_pb2_grpc.CommandExecutorServicer):
    def ExecuteCommand(self, request, context):
        try:
            process = subprocess.Popen(
                [request.command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                start_new_session=True,
                shell=True
            )
            return command_pb2.CommandResponse(
                status="running",
                output=f"{process.pid}"
            )
        except Exception as e:
            return command_pb2.CommandResponse(
                status="error",
                output=str(e),
            )

    def KillProcess(self, request, context):
        try:
            pid = int(request.command)
            os.kill(pid, signal.SIGTERM)
            return command_pb2.CommandResponse(
                status="terminated",
                output=f"Process with PID {pid} has been terminated"
            )
        except ProcessLookupError:
            return command_pb2.CommandResponse(
                status="error",
                output=f"Process with PID {pid} does not exist"
            )
        except Exception as e:
            return command_pb2.CommandResponse(
                status="error",
                output=str(e),
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    command_pb2_grpc.add_CommandExecutorServicer_to_server(CommandExecutorServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()