# grpc

# 1. Build
python -m grpc_tools.protoc -I. --python_out=./ --grpc_python_out=./ command.proto

# 2. Poetry env
poetry lock
poetry install
poetry shell
chmod +x src
cd src
poetry run python server.py

# 3. Ec2
pip install protobuf=="4.21.12"
pip install grpcio-tools=="1.56.2"
pip install grpcio=="1.56.2"
python3 server.py