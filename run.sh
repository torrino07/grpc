#!/bin/bash

# Lock and set up the environment
cd src
uv lock
uv venv
source .venv/bin/activate

# Compile protobuf
uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. command.proto

# Start FastAPI server in the background
uv run -- uvicorn server:app --reload &
FASTAPI_PID=$!

# Start gRPC server in the background
uv run python main.py &
GRPC_PID=$!

# Wait for both to finish (optional)
wait $FASTAPI_PID $GRPC_PID
