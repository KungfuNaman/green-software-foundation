#!/bin/bash
set -e

echo "starting script ..."

### Create a user for Ollama:
#useradd -r -s /bin/false -m -d /usr/share/ollama ollama

# Create a user for Ollama if it does not exist
if id "ollama" &>/dev/null; then
    echo "User 'ollama' already exists"
else
    echo "Creating user for Ollama..."
    useradd -r -s /bin/false -m -d /usr/share/ollama ollama || { echo "Failed to create user"; exit 1; }
fi
echo "-- Ollama User Created! --"

## Create a service file in /etc/systemd/system/ollama.service:
tee /etc/systemd/system/ollama.service > /dev/null <<EOL
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOL
echo "-- Service File Created! --"

## Then start the service:

apt-get install -y systemd
echo "-- Systemd installed! --"
#exec /lib/systemd/systemd
#echo "-- Systemd executed! --"

systemctl daemon-reload
echo "-- daemon reload! --"
systemctl enable ollama
echo "-- ollama enabled! --"
systemctl start ollama || { echo "Failed to start ollama"; exit 1; }

## Directly start the Ollama service without systemd
#nohup /usr/bin/ollama serve > /var/log/ollama.log 2>&1 &
#if [ $? -ne 0 ]; then
#  echo "Failed to start ollama"
#  exit 1
#fi

echo "ollama service started!"

# Run models
ollama pull llama2 || { echo "Failed to pull llama2"; exit 1; }
echo "llama2 pulled successfully!"
ollama pull phi3 || { echo "Failed to pull phi3"; exit 1; }
echo "phi3 pulled successfully!"
ollama pull llava || { echo "Failed to pull llava"; exit 1; }
echo "llava pulled successfully!"

# Start backend port
python main.py || { echo "Failed to start backend"; exit 1; }
echo "backend should be started from now"