# grpc

# 1. Build
python -m grpc_tools.protoc -I. --python_out=./src --grpc_python_out=./src command.proto

# 2. Poetry env
poetry lock
poetry install
poetry shell
chomd -777cchmod +x src/server.py
poetry run python src/server.py
