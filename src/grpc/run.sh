#!/bin/bash

sudo rm -rf /grpc/src/.venv

uv lock
uv venv
source .venv/bin/activate
uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. command.proto
uv run python main.py
