# grpc

# 1. Build
python -m grpc_tools.protoc -I. --python_out=./src --grpc_python_out=./src command.proto

# 2. Poetry env
poetry lock
poetry install
poetry shell
chmod +x src
cd src
poetry run python server.py
