# RAG APPLICATION

### Docker Images Download
1. make sure installed "Docker Desktop" in your machine
2. login 
```bash
docker login
```
3. pull backend & frontend images
```bash
docker pull yile785/green-software-foundation-backend:first
docker pull yile785/green-software-foundation-frontend:first
```
4. run the containers
```bash
# start containers separately
docker run -d -p 8000:8000 yile785/green-software-foundation-backend:first
docker run -d -p 3000:3000 yile785/green-software-foundation-frontend:first

# or use docker-compose.yml(in proj root dir) to run them in one go
docker-compose up
```

## Development
### Local Ollama Install
Install ollama https://www.ollama.com/ to local environment
- Ollama commands (ollama list: to see the downloaded models, these models are saved in the home directory under .ollama)

Check if Ollama is configured
```bash
ollama --version
```

Pull llama2 model and chat
```bash
ollama run llama2
```

### To run backend 
```bash
python Rag/api.py
```
Request will be served on port 8000

### To run frontend





