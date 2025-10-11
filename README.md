# LangChain with Ollama Demo

This project demonstrates the integration of LangChain with Ollama for AI/ML applications, featuring a FastAPI backend with Swagger documentation and Docker support.

## Quick Start

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd first

# Make the initialization script executable
chmod +x scripts/init-ollama.sh

# Start the application (this will automatically download the llama2 model)
docker-compose up -d

# Check if services are healthy
curl http://localhost:8000/health

# View the API documentation
open http://localhost:8000/docs

# View startup progress
docker-compose logs -f

# Stop the application
docker-compose down
```

## System Requirements

- Docker Engine 20.10.0 or newer
- Docker Compose 2.0.0 or newer
- Minimum 4GB RAM
- At least 10GB free disk space (for Docker images and LLM model)

## Project Structure

```
.
├── README.md
├── requirements.txt
├── main.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── scripts/
│   └── init-ollama.sh      # Ollama initialization script
└── app/
    ├── __init__.py
    ├── routers/
    │   ├── __init__.py
    │   └── chat_router.py  # Chat API endpoints
    └── services/
        ├── __init__.py
        └── llm_service.py  # LLM integration service
```

### Key Components

- `scripts/init-ollama.sh`: Handles Ollama service initialization and model download
- `docker-compose.yml`: Defines and configures the application services
- `app/services/llm_service.py`: Manages LLM interactions and health checks
- `app/routers/chat_router.py`: Implements the chat API endpoints

## Prerequisites

1. Docker and Docker Compose installed on your system
   - Install from [Docker's official website](https://docs.docker.com/get-docker/)
   - Minimum requirements:
     - Docker Engine 20.10.0 or newer
     - Docker Compose 2.0.0 or newer
   - Recommended system resources:
     - 4GB RAM minimum
     - 10GB free disk space

## Project Management

### Starting the Project

1. **First-time setup**:
   ```bash
   # Clone the repository (if not already done)
   git clone <repository-url>
   cd first
   
   # Build and start containers in detached mode
   docker-compose up -d --build
   
   # Wait for services to initialize (including model download)
   # You can check the model download progress with:
   docker-compose logs -f ollama
   
   # Verify services are running
   docker-compose ps
   
   # Verify model is loaded and API is ready
   curl http://localhost:8000/health
   ```

2. **Regular startup** (after first-time setup):
   ```bash
   # Start services in detached mode
   docker-compose up -d
   ```

3. **Development mode** (with logs):
   ```bash
   # Start services in foreground with logs
   docker-compose up
   ```

### Monitoring and Logs

1. **View logs for all services**:
   ```bash
   # Follow logs in real-time
   docker-compose logs -f
   
   # View last 100 lines
   docker-compose logs --tail=100
   ```

2. **View logs for specific service**:
   ```bash
   # Follow API service logs
   docker-compose logs -f api
   
   # Follow Ollama service logs
   docker-compose logs -f ollama
   ```

3. **Check service status**:
   ```bash
   docker-compose ps
   ```

### Stopping the Project

1. **Graceful shutdown** (preserves data):
   ```bash
   # Stop services
   docker-compose down
   
   # Stop services and remove volumes (will delete stored models)
   docker-compose down -v
   ```

2. **Force shutdown** (in case of issues):
   ```bash
   docker-compose down --timeout 0
   ```

### Maintenance

1. **Rebuild services** (after dependency changes):
   ```bash
   # Rebuild specific service
   docker-compose build api
   
   # Rebuild all services
   docker-compose build
   ```

2. **Reset environment**:
   ```bash
   # Remove all containers, volumes, and cached images
   docker-compose down -v --rmi all
   ```

3. **Update models**:
   ```bash
   # Access Ollama container
   docker-compose exec ollama bash
   
   # Pull latest model version
   ollama pull llama2
   ```

### Troubleshooting

1. **If services won't start**:
   ```bash
   # Check service logs
   docker-compose logs
   
   # Verify port availability
   lsof -i :8000
   lsof -i :11434
   ```

2. **If API is unresponsive**:
   ```bash
   # Restart API service
   docker-compose restart api
   
   # Check API health
   curl http://localhost:8000/health
   ```

3. **If Ollama is slow**:
   ```bash
   # Check Ollama resource usage
   docker stats ollama
   ```

## Running with Docker

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
   This will:
   - Build the FastAPI application container
   - Pull and start the Ollama container
   - Set up the necessary networking between containers
   - Mount the required volumes

2. Access the Swagger documentation at: http://localhost:8000/docs

3. The Ollama service will automatically pull and use the llama2 model

To stop the application:
```bash
docker-compose down
```

## Running Locally (Alternative)

If you prefer to run the application without Docker:

1. Install Ollama on your system
   - Install from [Ollama's official website](https://ollama.ai)
   - Run: `ollama pull llama2`

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set the Ollama host environment variable:
   ```bash
   export OLLAMA_HOST=http://localhost:11434
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

- **POST /api/v1/chat**
  - Send a message to the LLM and get a response
  - Request body: `{"message": "Your message here"}`

## API Usage

### Chat Endpoint

**Endpoint**: `POST /api/v1/chat`

**Request Format**:
```json
{
    "message": "What is artificial intelligence?"
}
```

**Response Format**:
```json
{
    "response": "Artificial Intelligence (AI) is..."
}
```

**Example using curl**:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is artificial intelligence?"}'
```

### Health Check Endpoint

**Endpoint**: `GET /health`

**Response Format**:
```json
{
    "status": "healthy",
    "api": {
        "status": "running",
        "version": "1.0.0"
    },
    "ollama": {
        "status": "healthy",
        "models": 1,
        "model_ready": true,
        "target_model": "llama2"
    }
}
```

## Troubleshooting

### Common Issues

1. **Services won't start**:
   ```bash
   # Check service logs
   docker-compose logs
   
   # Verify port availability
   lsof -i :8000
   lsof -i :11434
   ```

2. **API returns 500 error**:
   - Check if Ollama service is healthy
   - Verify model is downloaded
   - Check API logs: `docker-compose logs api`

3. **Slow responses**:
   - First request might be slow due to model loading
   - Check resource usage: `docker stats`

4. **Model download issues**:
   ```bash
   # Check Ollama logs
   docker-compose logs ollama
   
   # Restart Ollama service
   docker-compose restart ollama
   ```

### Maintenance

1. **Clear all data and restart**:
   ```bash
   docker-compose down -v
   docker-compose up -d --build
   ```

2. **Update the model**:
   ```bash
   docker-compose exec ollama ollama pull llama2
   docker-compose restart api
   ```

## Development

### Local Development Setup

1. Start services in development mode:
   ```bash
   docker-compose up
   ```

2. View real-time logs while developing:
   ```bash
   docker-compose logs -f
   ```

3. After code changes:
   ```bash
   docker-compose up -d --build
   ```

### Best Practices

1. Always check the health endpoint before sending requests
2. Monitor logs during development
3. Use Swagger UI for testing API endpoints
4. Check service status with `docker-compose ps`

## Development

The project uses:
- FastAPI for the web framework
- LangChain for LLM integration
- Ollama for local LLM hosting
- Pydantic for data validation