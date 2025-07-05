# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:yes
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)

base64 -i config.toml
base64 -i config.toml -o config
base64 -d -i config -o config.toml


uv lock
uv venv
source .venv/bin/activate
uv run -- uvicorn client:app --reload
## grpc
uv lock
uv venv
source .venv/bin/activate
uv run python server.py

poetry run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. command.proto
poetry run python server.py
poetry run -- uvicorn client:app --reload
poetry run python test.py


sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
sudo ln -s /usr/bin/python3.11 /usr/local/bin/python

sudo systemctl list-units --type=service | grep feeds@



sudo cp feeds@.service /etc/systemd/system/
sudo cp feeds /opt/hft/bin/feeds

sudo chmod +x /opt/hft/bin/feeds

sudo systemctl stop feeds@binance.spot
sudo systemctl disable feeds@binance.spot
sudo rm -f /etc/feeds/binance.spot.env
sudo rm -rf /etc/systemd/system/feeds@binance.spot.service.d
sudo rm -f /etc/systemd/system/feeds@.service
sudo systemctl daemon-reload
sudo systemctl reset-failed

sudo journalctl -xeu feeds@binance.spot.service

lsof -i :5555 -t | xargs kill -9
lsof -i :5558 -t | xargs kill -9
lsof -i :5559 -t | xargs kill -9

pgrep -f feeds

brew install colima 
colima start --arch aarch64 --cpu 6 --memory 8
colima ssh

colima stop
colima start --mount $PWD:/grpc
colima ssh
cd /grpc

poetry lock
poetry install

poetry run python systemd.py
poetry run python test.py


# Check if process is pinned to core ##
systemctl status feeds@binance.spot.service
pid -> 2505
cat /proc/2505/status | grep Cpus_allowed_list



uv lock
uv venv
source .venv/bin/activate
uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. command.proto
uv run -- uvicorn server:app --reload

uv lock
uv venv
source .venv/bin/activate
uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. command.proto
uv run python main.py