#!/bin/sh

# Get model names from environment variables or use defaults
BASE_MODEL=${BASE_MODEL:-llama2}
TARGET_MODEL=${TARGET_MODEL:-llama3}
MODEL_PARAMS=${MODEL_PARAMS:-'{"temperature":0.7,"top_k":50,"top_p":0.7,"num_ctx":4096}'}

# Start Ollama service
ollama serve &

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to start..."
until curl -s -f "http://localhost:11434/api/tags" > /dev/null 2>&1; do
    echo "Waiting for Ollama service..."
    sleep 2
done

echo "Ollama service is up, setting up models..."

# First ensure base model is available
echo "Checking for ${BASE_MODEL} model..."
if ! curl -s "http://localhost:11434/api/tags" | grep -q "${BASE_MODEL}"; then
    echo "Pulling ${BASE_MODEL} model..."
    ollama pull ${BASE_MODEL}
    echo "${BASE_MODEL} model pull completed"
else
    echo "${BASE_MODEL} model already exists"
fi

# Check if target model already exists
echo "Checking for ${TARGET_MODEL} model..."
if ! curl -s "http://localhost:11434/api/tags" | grep -q "${TARGET_MODEL}"; then
    echo "Creating ${TARGET_MODEL} model from ${BASE_MODEL}..."
    
    # Extract parameters from MODEL_PARAMS
    TEMP=$(echo $MODEL_PARAMS | jq -r '.temperature // 0.7')
    TOP_K=$(echo $MODEL_PARAMS | jq -r '.top_k // 50')
    TOP_P=$(echo $MODEL_PARAMS | jq -r '.top_p // 0.7')
    NUM_CTX=$(echo $MODEL_PARAMS | jq -r '.num_ctx // 4096')
    
    # Create Modelfile with parameters
    cat > /tmp/Modelfile << EOF
FROM ${BASE_MODEL}
PARAMETER stop </s>
PARAMETER stop [INST]
PARAMETER temperature ${TEMP}
PARAMETER top_k ${TOP_K}
PARAMETER top_p ${TOP_P}
PARAMETER num_ctx ${NUM_CTX}

SYSTEM You are an AI assistant running on ${TARGET_MODEL}, an upgraded version of ${BASE_MODEL}. You are helpful, respectful, and honest.
EOF
    
    # Create the model
    ollama create ${TARGET_MODEL} -f /tmp/Modelfile
    echo "${TARGET_MODEL} model creation completed"
else
    echo "${TARGET_MODEL} model already exists"
fi

# Keep container running
tail -f /dev/null