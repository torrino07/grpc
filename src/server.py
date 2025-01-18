from concurrent import futures
import grpc
import subprocess
import os
import signal
import command_pb2
import command_pb2_grpc
import logging
import argparse
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

parser = argparse.ArgumentParser(description="Port Parameter")
parser.add_argument("--port", help="The first argument")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CommandExecutorServicer(command_pb2_grpc.CommandExecutorServicer):
    def ExecuteCommand(self, request, context):
        args = request.command
        print(args)
        try:
            process = subprocess.Popen(
                ["./Feeds"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                start_new_session=True,
                shell=False,
                encoding="utf-8"
            )
            process.stdin.write(args)
            process.stdin.close()
     
            logging.info("Started process with PID: %d", process.pid)
            return command_pb2.CommandResponse(
                status="running",
                output=f"{process.pid}"
            )
        except Exception as e:
            logging.error("Error executing command: %s", str(e))
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
    server.add_insecure_port(f"[::]:{args.port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()