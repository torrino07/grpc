import locale
import logging
import os
import signal
import subprocess
from concurrent import futures

import command_pb2
import command_pb2_grpc

import grpc

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CommandExecutorServicer(command_pb2_grpc.CommandExecutorServicer):
    def ExecuteCommand(self, request, context):
        executable = request.executable
        args = request.command
        try:
            process = subprocess.Popen(
                [executable] + [args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                start_new_session=True,
                shell=False,
                encoding='utf-8'
            )
            process.stdin.write(args)
            process.stdin.close()

            logging.info("Started process with PID: %d", process.pid)
            return command_pb2.CommandResponse(status="running", output=f"{process.pid}")
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
            try:
                os.waitpid(pid, 0)
            except ChildProcessError:
                pass
            return command_pb2.CommandResponse(
                status="terminated", output=f"Process with PID {pid} has been terminated"
            )
        except ProcessLookupError:
            return command_pb2.CommandResponse(status="error", output=f"Process with PID {pid} does not exist")
        except Exception as e:
            return command_pb2.CommandResponse(
                status="error",
                output=str(e),
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    command_pb2_grpc.add_CommandExecutorServicer_to_server(CommandExecutorServicer(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
