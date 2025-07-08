colima stop
colima start --arch aarch64 --cpu 6 --memory 8 --mount $PWD:/grpc:w
colima ssh << 'EOF'
curl -Ls https://astral.sh/uv/install.sh | sh
sudo cp feeds@.service /etc/systemd/system/
sudo cp feeds /opt/hft/bin/feeds
sudo chmod +x /opt/hft/bin/feeds
cd /grpc
EOF


# echo "🛑 Stopping Colima (if running)..."
# colima stop || true

# echo "🚀 Starting Colima with custom config..."
# colima start --arch aarch64 --cpu 8 --memory 8 --disk 100 --mount $PWD:/server:w

# echo "🔐 Bootstrapping environment inside Colima..."
# colima ssh << 'EOF'

# sudo apt-get update
# sudo apt-get install -y lsof

# echo "1. 🌐 Installing uv (Python package manager)..."
# echo 'export UV_LINK_MODE=copy' >> ~/.bashrc
# curl -Ls https://astral.sh/uv/install.sh | sh

# echo "2. 🐘 Installing PostgreSQL 14..."
# curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | sudo tee /usr/share/keyrings/postgresql.gpg > /dev/null
# echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list > /dev/null

# sudo apt-get update
# sudo apt-get install -y postgresql-14 postgresql-client-14

# echo "host all postgres 0.0.0.0/0 trust" | sudo tee /etc/postgresql/14/main/pg_hba.conf > /dev/null

# PG_CONF="/etc/postgresql/14/main/postgresql.conf"
# sudo sed -i "s/^#listen_addresses = 'localhost'/listen_addresses = '*'/g" "$PG_CONF"

# sudo systemctl restart postgresql

# echo "3. 🟦 Installing Node.js and npm..."
# curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
# sudo apt-get install -y nodejs

# echo "4. 📁 Setting up systemd service and binary..."
# cd /server
# sudo mkdir -p /opt/hft/bin
# sudo cp feeds@.service /etc/systemd/system/
# sudo cp feeds /opt/hft/bin/feeds
# sudo chmod +x /opt/hft/bin/feeds

# echo "✅ Environment setup complete inside Colima."
# EOF
# colima ssh