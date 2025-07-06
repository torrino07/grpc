#!/bin/bash

sudo rm -rf /grpc/src/.venv

# Move into the source directory
cd src

# Lock dependencies and create virtual environment
uv lock
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Compile protobuf definitions
echo "Compiling command.proto..."
uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. command.proto

echo "✅ Protobuf compiled successfully."

# Start gRPC server in the background
echo "Starting gRPC server..."
uv run python main.py &
GRPC_PID=$!

sleep 2

# Start FastAPI server in the background
echo "Starting FastAPI server..."
uv run uvicorn server:app --reload &
FASTAPI_PID=$!

# Wait for gRPC server to finish first
wait $GRPC_PID

# Optionally stop FastAPI if gRPC exits
kill $FASTAPI_PID 2>/dev/null || true

#rm -rf /grpc/src/.venv
