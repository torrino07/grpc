colima stop
colima start --arch aarch64 --cpu 6 --memory 8 --mount $PWD:/grpc:w
colima ssh << 'EOF'
curl -Ls https://astral.sh/uv/install.sh | sh
cd /grpc
sudo cp feeds@.service /etc/systemd/system/
sudo cp feeds /opt/hft/bin/feeds
sudo chmod +x /opt/hft/bin/feeds
EOF
colima ssh