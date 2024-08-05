FROM python:3.8

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

# Install ollama
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install systemd, sudo, and create ollama user
RUN apt-get update && apt-get install -y \
    systemd \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create ollama user
RUN if id "ollama" &>/dev/null; then \
    echo "User 'ollama' already exists"; \
else \
    echo "Creating user for Ollama..."; \
    useradd -r -s /bin/false -m -d /usr/share/ollama ollama || { echo "Failed to create user"; exit 1; }; \
fi

## Create and configure ollama service
#RUN tee /etc/systemd/system/ollama.service > /dev/null <<EOL
#[Unit]
#Description=Ollama Service
#After=network-online.target
#
#[Service]
#ExecStart=/usr/bin/ollama serve
#User=ollama
#Group=ollama
#Restart=always
#RestartSec=3
#
#[Install]
#WantedBy=default.target
#EOL

# Create and configure ollama service
RUN echo "[Unit]\n\
Description=Ollama Service\n\
After=network-online.target\n\
\n\
[Service]\n\
ExecStart=/usr/bin/ollama serve\n\
User=ollama\n\
Group=ollama\n\
Restart=always\n\
RestartSec=3\n\
\n\
[Install]\n\
WantedBy=default.target" > /etc/systemd/system/ollama.service

# Create supervisor configuration file
RUN echo "[supervisord]\n\
nodaemon=true\n\
\n\
[program:ollama]\n\
command=/usr/bin/ollama serve\n\
user=ollama\n\
autostart=true\n\
autorestart=true\n\
stdout_logfile=/var/log/ollama.log\n\
stderr_logfile=/var/log/ollama.err" > /etc/supervisor/conf.d/ollama.conf

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]

## Reload systemd daemon and enable ollama service
#RUN systemctl daemon-reload && \
#    systemctl enable ollama
## Start ollama service
#RUN systemctl start ollama || { echo "Failed to start ollama"; exit 1; }

# Pull required models
RUN ollama pull llama2 || { echo "Failed to pull llama2"; exit 1; } && \
    ollama pull phi3 || { echo "Failed to pull phi3"; exit 1; } && \
    ollama pull llava || { echo "Failed to pull llava"; exit 1; }

# Set the working directory to /app
WORKDIR /app

# Run the backend
CMD ["python", "main.py"]


# Copy start script
#COPY start_backend.sh /start_backend.sh
#RUN chmod +x /start_backend.sh

## Copy the entrypoint script
#COPY entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh
#
#VOLUME [ "/sys/fs/cgroup" ]
#STOPSIGNAL SIGRTMIN+3

#EXPOSE 8000

## Set default command to start systemd and our script
#ENTRYPOINT [ "/entrypoint.sh" ]

## Start Backend
#CMD ["/start_backend.sh"]