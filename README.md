# grpc

# 1. Build
python -m grpc_tools.protoc -I. --python_out=./ --grpc_python_out=./ command.proto

# 2. Poetry env
poetry lock
poetry install
poetry shell
chmod +x src
cd src
poetry run python server.py --port 50052

# 3. Ec2
pip install protobuf=="4.21.12"
pip install grpcio-tools=="1.59.0"
pip install grpcio=="1.59.0"
python3 server.py

uvicorn client:app --host 0.0.0.0 --port 8000 --reload

curl -k -X POST http://0.0.0.0:8000/api/v1/processes/start \
     -H "Content-Type: application/json" \
     -d '{"host":"stream.binance.com", "port": 443, "request": {"method": "SUBSCRIBE","params": ["ethusdt@bookTicker", "ethusdt@trade"],"id": 1}, "handshake": "/stream?streams=", "topic": "binance.spot.raw", "client": "redis", "clientHost": "127.0.0.1", "clientPort": 6379}'

ps aux | grep ./Feeds | grep -v grep | awk '{print $2}' | xargs kill -9