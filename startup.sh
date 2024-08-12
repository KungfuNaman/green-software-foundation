#!/bin/bash

# Wait for 5 seconds before starting the service
echo "Waiting for 5 seconds before starting the service..."
sleep 5

# Start the Ollama service in the background
echo "Starting Ollama service..."
ollama serve &

# Wait for Ollama service to be fully up
echo "Waiting for Ollama service to be fully up..."
while ! curl -s http://localhost:11434 &> /dev/null; do
    echo "Waiting for Ollama service to start..."
    sleep 5
done

echo "Ollama service is up and running."

# Pull the phi3 model
echo "Pulling llama2 model..."
ollama pull llama2

# Create a new model using the provided Modelfile
echo "Creating a new model with the name 'fineTunedModel'..."
ollama create "fineTunedModel" -f /root/Modelfile

echo "Fine tuned model up and running in ollama"

# Keep the service running
wait
