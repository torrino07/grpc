# grpc

# 1. Start Virtual env locally
pip install virtualenv
virtualenv env
source env/bin/activate 
pip install -r requirements.txt

pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. command.proto
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


curl -X POST http://127.0.0.1:8000/start -H "Content-Type: application/json"

curl -X DELETE http://127.0.0.1:8000/stop/15492