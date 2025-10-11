#!/bin/sh

# Start Ollama service
ollama serve &

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to start..."
until curl -s -f "http://localhost:11434/api/tags" > /dev/null 2>&1; do
    echo "Waiting for Ollama service..."
    sleep 2
done

echo "Ollama service is up, checking for llama2 model..."

# Check if model exists
if ! curl -s "http://localhost:11434/api/tags" | grep -q "llama2"; then
    echo "Pulling llama2 model..."
    ollama pull llama2
    echo "Model pull completed"
else
    echo "llama2 model already exists"
fi

# Keep container running
tail -f /dev/null