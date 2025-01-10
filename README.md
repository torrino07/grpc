# grpc

# 1. Start Virtual env locally
pip install virtualenv
virtualenv env
source env/bin/activate 
pip install -r requirements.txt

pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I. --python_out=./src --grpc_python_out=./src command.proto
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


curl -X POST http://127.0.0.1:8000/api/v1/processes/start -H "Content-Type: application/json"

curl -X DELETE http://127.0.0.1:8000/api/v1/processes/stop/15492

curl -X POST http://127.0.0.1:8000/api/v1/processes/start \
     -H "Content-Type: application/json" \
     -d '{"host":"stream.binance.com", "port": 443, "request": {"method": "SUBSCRIBE","params": ["btcusdt@depth@100ms", "btcusdt@trade"],"id": 1}, "handshake": "/stream?streams=", "topic": "binance.spot.raw", "client": "zeromq", "clientHost": "127.0.0.1", "clientPort": 5556}'

curl -k -X DELETE http://127.0.0.1:8000/api/v1/processes/stop/76114

lsof -i :5556