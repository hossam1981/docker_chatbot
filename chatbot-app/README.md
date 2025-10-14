# 🤖 Docker Chatbot Application

A full-stack chatbot application powered by Docker containers. This project demonstrates a microservices architecture using Python Flask for the chatbot logic, MongoDB for persistent storage, Redis for caching, NGINX as a reverse proxy, and a mock LLaMA API for generating intelligent responses.

## 📦 Technologies Used

- **Python (Flask)** – Chatbot API and web service
- **MongoDB** – Persistent storage for chat history
- **Redis** – In-memory caching for faster response times
- **NGINX** – Reverse proxy and load balancer
- **Docker Compose** – Multi-container orchestration
- **LLaMA Mock API** – Simulates Large Language Model responses

## 📁 Project Structure

```
chatbot-app/
├── app/
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
├── llamaapi/
│   ├── app.py              # Mock LLaMA API service
│   ├── Dockerfile          # LLaMA API container config
│   └── requirements.txt    # LLaMA API dependencies
├── nginx/
│   └── default.conf        # NGINX configuration
├── Dockerfile              # Main app container config
├── docker-compose.yml      # Multi-container orchestration
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system
- Basic knowledge of REST APIs and JSON

### Installation & Running

1. **Clone or navigate to the project directory:**
   ```bash
   cd chatbot-app
   ```

2. **Build and start all containers:**
   ```bash
   docker-compose up --build
   ```

3. **Verify all services are running:**
   ```bash
   docker-compose ps
   ```

4. **Access the chatbot:**
   - **API Endpoint:** `http://localhost:8080/chat`
   - **Direct Flask App:** `http://localhost:5000/chat` (if ports are exposed)
   - **MongoDB:** `localhost:27017`
   - **Redis:** `localhost:6379`
   - **LLaMA API:** `http://localhost:8000/generate`

## 🧪 Testing the Application

### Using curl

```bash
curl -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"Hello, how are you?"}'
```

### Using Postman

1. Set method to `POST`
2. URL: `http://localhost:8080/chat`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "message": "What's the weather like today?"
   }
   ```

### Expected Response

```json
{
  "response": "LLaMA says: What's the weather like today?"
}
```

## 🧠 Architecture Overview

### Service Components

1. **Flask App (`chatbot`)** 
   - Handles `/chat` endpoint
   - Integrates with Redis for caching
   - Stores chat history in MongoDB
   - Communicates with LLaMA API

2. **Redis (`redis`)**
   - Caches chatbot responses for faster retrieval
   - Reduces load on the LLaMA API
   - Improves response times for repeated queries

3. **MongoDB (`mongo`)**
   - Stores complete chat history
   - Enables analytics and conversation tracking
   - Provides data persistence across container restarts

4. **LLaMA API (`llama`)**
   - Generates intelligent responses (currently mocked)
   - Can be replaced with real LLM integration
   - Handles natural language processing

5. **NGINX (`nginx`)**
   - Routes external traffic to Flask app
   - Provides load balancing capabilities
   - Adds security layer and SSL termination (when configured)

### Data Flow

```
User Request → NGINX → Flask App → Redis Cache Check
                                    ↓
                              Cache Miss → LLaMA API
                                    ↓
                              Store in Redis & MongoDB → Response
```

## 🔧 Configuration

### Environment Variables

You can customize the application by modifying the `docker-compose.yml` file:

- **Ports:** Change exposed ports in the `ports` section
- **Database:** Modify MongoDB connection strings
- **Cache:** Adjust Redis configuration
- **API:** Update LLaMA API endpoints

### NGINX Configuration

The NGINX configuration (`nginx/default.conf`) can be modified to:
- Add SSL certificates
- Configure load balancing
- Set up rate limiting
- Add authentication headers

## 🛠️ Development

### Adding Real LLaMA Integration

To integrate a real LLaMA model, modify `llamaapi/app.py`:

```python
# Replace the mock response with actual model calls
# Example using transformers library:
from transformers import LlamaTokenizer, LlamaForCausalLM

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.json.get("prompt")
    # Add your LLaMA model logic here
    response = model.generate(prompt)
    return jsonify({"response": response})
```

### Adding a Frontend

Create a new service in `docker-compose.yml`:

```yaml
frontend:
  build: ./frontend
  ports:
    - "3000:3000"
  depends_on:
    - chatbot
  networks:
    - backend
```

## 📊 Monitoring & Logs

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs chatbot
docker-compose logs mongo
docker-compose logs redis
```

### Monitor Performance

```bash
# Container stats
docker stats

# Service health
docker-compose ps
```

## 🚀 Future Enhancements

- [ ] **Real LLM Integration** – Replace mock API with actual LLaMA, GPT, or Claude
- [ ] **Frontend UI** – Add React, Vue, or Angular frontend
- [ ] **Authentication** – Implement user sessions and JWT tokens
- [ ] **Cloud Deployment** – Deploy to AWS, Azure, or GCP
- [ ] **Database Scaling** – Add MongoDB replica sets
- [ ] **Caching Strategy** – Implement Redis clustering
- [ ] **API Rate Limiting** – Add request throttling
- [ ] **Monitoring** – Integrate Prometheus and Grafana
- [ ] **CI/CD Pipeline** – Automated testing and deployment
- [ ] **Multi-language Support** – Internationalization features

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check if ports are in use
   netstat -tulpn | grep :8080
   # Change ports in docker-compose.yml if needed
   ```

2. **Container Won't Start**
   ```bash
   # Check logs
   docker-compose logs [service-name]
   # Rebuild containers
   docker-compose up --build --force-recreate
   ```

3. **Database Connection Issues**
   ```bash
   # Verify MongoDB is running
   docker-compose exec mongo mongosh
   # Check network connectivity
   docker-compose exec chatbot ping mongo
   ```

### Clean Up

```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Check the troubleshooting section above
- Review Docker and Docker Compose documentation

---

**Happy Chatting! 🎉**
