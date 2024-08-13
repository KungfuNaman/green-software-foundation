# Base image
FROM ollama/ollama:0.1.32

# Install required packages
RUN apt-get update && \
    apt-get install -y curl python3-pip && \
    apt-get install -y iputils-ping && \
    pip3 install gdown && \
    rm -rf /var/lib/apt/lists/*

    # Set working directory
WORKDIR /root/.ollama

# Copy the model file and gguf file into the container
COPY Modelfile /root/Modelfile
RUN gdown --id 101grZBeyvPng_kW03uZLUVboW2fvakrj -O /root/fineTunedModel.gguf

# Copy the startup script into the container
COPY startup.sh /root/startup.sh

# Make sure the script is executable
RUN chmod +x /root/startup.sh

# Set the script as the entrypoint~
ENTRYPOINT ["bash", "/root/startup.sh"]
