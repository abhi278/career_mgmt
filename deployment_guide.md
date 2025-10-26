# Deployment Guide 🚀

Complete guide for deploying the Resume Analyzer application in various environments.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Local Development

### Setup

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd resume-analyzer
```

2. **Create virtual environment**:
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
# Using uv
uv pip install -e ".[dev]"

# Or using pip
pip install -e ".[dev]"
```

4. **Configure environment**:
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

5. **Run the application**:
```bash
python app.py
```

Visit `http://localhost:8050` in your browser.

### Development Mode Features

- Hot reloading enabled
- Debug mode active
- Detailed error messages
- Source code mounted in Docker (if using Docker)

## Docker Deployment

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

### Quick Start

1. **Prepare environment file**:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

2. **Build and start**:
```bash
docker-compose up -d --build
```

3. **Verify deployment**:
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f resume-analyzer

# Test application
curl http://localhost:8050
```

### Docker Commands Cheat Sheet

```bash
# Build without cache
docker-compose build --no-cache

# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# Stop containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Restart specific service
docker-compose restart resume-analyzer

# View logs (last 100 lines)
docker-compose logs --tail=100 resume-analyzer

# Follow logs in real-time
docker-compose logs -f resume-analyzer

# Execute command in container
docker-compose exec resume-analyzer bash

# View resource usage
docker stats resume-analyzer-app
```

### Docker Configuration

#### Modify Port Mapping

Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:8050"  # External:Internal
```

#### Adjust Resources

Add to `docker-compose.yml`:
```yaml
services:
  resume-analyzer:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

#### Production Configuration

For production, modify `docker-compose.yml`:
```yaml
services:
  resume-analyzer:
    # Remove volume mounts for code
    # volumes:
    #   - ./src:/app/src
    #   - ./app.py:/app/app.py
    
    # Add environment variables
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEBUG=False
      - WORKERS=4
    
    # Add restart policy
    restart: always
```

## Production Deployment

### Option 1: Standalone Docker Deployment

1. **Prepare production environment**:
```bash
# Create production env file
cat > .env.production << EOF
OPENAI_API_KEY=your-production-api-key
PYTHONUNBUFFERED=1
DEBUG=False
EOF
```

2. **Build production image**:
```bash
docker build -t resume-analyzer:production .
```

3. **Run production container**:
```bash
docker run -d \
  --name resume-analyzer \
  --env-file .env.production \
  -p 8050:8050 \
  --restart unless-stopped \
  --memory 2g \
  --cpus 2 \
  resume-analyzer:production
```

### Option 2: With Nginx Reverse Proxy

1. **Install Nginx**:
```bash
sudo apt-get update
sudo apt-get install nginx
```

2. **Create Nginx configuration** (`/etc/nginx/sites-available/resume-analyzer`):
```nginx
upstream resume_analyzer {
    server localhost:8050;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://resume_analyzer;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        proxy_pass http://resume_analyzer;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

3. **Enable site and restart Nginx**:
```bash
sudo ln -s /etc/nginx/sites-available/resume-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. **Add SSL with Let's Encrypt**:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Option 3: Systemd Service

1. **Create systemd service** (`/etc/systemd/system/resume-analyzer.service`):
```ini
[Unit]
Description=Resume Analyzer Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/resume-analyzer
Environment="PATH=/opt/resume-analyzer/venv/bin"
EnvironmentFile=/opt/resume-analyzer/.env
ExecStart=/opt/resume-analyzer/venv/bin/gunicorn \
    --bind 0.0.0.0:8050 \
    --workers 4 \
    --timeout 120 \
    --access-logfile /var/log/resume-analyzer/access.log \
    --error-logfile /var/log/resume-analyzer/error.log \
    app:server

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. **Enable and start service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable resume-analyzer
sudo systemctl start resume-analyzer
sudo systemctl status resume-analyzer
```

## Cloud Deployment

### AWS EC2

1. **Launch EC2 instance**:
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (2 vCPU, 4GB RAM)
   - Security group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **Connect and setup**:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone <your-repo-url>
cd resume-analyzer

# Setup and deploy
cp .env.example .env
nano .env  # Add your API key
docker-compose up -d
```

### AWS ECS (Fargate)

1. **Push image to ECR**:
```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repository
aws ecr create-repository --repository-name resume-analyzer

# Build and push
docker build -t resume-analyzer .
docker tag resume-analyzer:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/resume-analyzer:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/resume-analyzer:latest
```

2. **Create ECS task definition** (task-definition.json):
```json
{
  "family": "resume-analyzer",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "resume-analyzer",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/resume-analyzer:latest",
      "portMappings": [
        {
          "containerPort": 8050,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/resume-analyzer",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

3. **Create and run service**:
```bash
# Create cluster
aws ecs create-cluster --cluster-name resume-analyzer-cluster

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster resume-analyzer-cluster \
  --service-name resume-analyzer-service \
  --task-definition resume-analyzer \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

### Google Cloud Run

1. **Build and push to GCR**:
```bash
# Configure gcloud
gcloud auth configure-docker

# Build image
docker build -t gcr.io/your-project-id/resume-analyzer .

# Push to GCR
docker push gcr.io/your-project-id/resume-analyzer
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy resume-analyzer \
  --image gcr.io/your-project-id/resume-analyzer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-api-key \
  --memory 2Gi \
  --cpu 2 \
  --timeout 120 \
  --max-instances 10
```

### Heroku

1. **Install Heroku CLI and login**:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

2. **Create and configure app**:
```bash
# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your-api-key

# Deploy
git push heroku main

# Scale
heroku ps:scale web=1:standard-2x
```

3. **Create `Procfile`**:
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:server
```

## Monitoring and Maintenance

### Health Checks

```bash
# Check application health
curl http://localhost:8050/

# Check Docker container health
docker ps
docker inspect resume-analyzer-app | grep Health
```

### Logs Management

```bash
# View Docker logs
docker-compose logs -f --tail=100

# View system logs (systemd)
sudo journalctl -u resume-analyzer -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backup and Recovery

```bash
# Backup environment configuration
cp .env .env.backup.$(date +%Y%m%d)

# Export Docker image
docker save resume-analyzer:latest | gzip > resume-analyzer-backup.tar.gz

# Import Docker image
docker load < resume-analyzer-backup.tar.gz
```

### Updates and Maintenance

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Or zero-downtime update
docker-compose up -d --no-deps --build resume-analyzer
```

### Performance Monitoring

Add monitoring tools:

1. **Prometheus + Grafana**:
```yaml
# Add to docker-compose.yml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

2. **Application metrics**:
```python
# Add to app.py
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app.server)
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs resume-analyzer

# Check if port is in use
sudo lsof -i :8050

# Restart Docker service
sudo systemctl restart docker
```

### High memory usage
```bash
# Check resource usage
docker stats

# Reduce workers in Dockerfile
# Change: --workers 4 to --workers 2
```

### API errors
```bash
# Verify API key
docker-compose exec resume-analyzer env | grep OPENAI

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## Security Best Practices

1. **Use secrets management** (AWS Secrets Manager, HashiCorp Vault)
2. **Enable HTTPS** with valid SSL certificates
3. **Implement rate limiting** (Nginx limit_req)
4. **Regular security updates**: `docker-compose pull && docker-compose up -d`
5. **Monitor logs** for suspicious activity
6. **Use non-root user** in Docker container
7. **Network isolation** with Docker networks
8. **Input validation** and file size limits

---

For more information, see the [README.md](README.md) file.
