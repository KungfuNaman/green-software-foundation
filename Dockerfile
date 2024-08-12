# Base image
FROM ollama/ollama

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /root/.ollama

# Copy the model file and gguf file into the container
COPY Modelfile /root/Modelfile
COPY fineTunedModels/fineTunedModel.gguf /root/fineTunedModel.gguf

# Copy the startup script into the container
COPY startup.sh /root/startup.sh

# Make sure the script is executable
RUN chmod +x /root/startup.sh

# Set the script as the entrypoint
ENTRYPOINT ["bash", "/root/startup.sh"]
