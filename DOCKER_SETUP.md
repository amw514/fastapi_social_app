# Docker Setup Guide

## Prerequisites
- Docker installed
- Docker Compose installed

## Quick Start

### 1. Create Environment File

Create a `.env` file in the project root with the following content:

```env
# For local development (without Docker)
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important:** When running with Docker, the `DATABASE_HOSTNAME` will be automatically set to `postgres` (the service name) in the docker-compose file.

### 2. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose -f docker-compose-dev.yml up --build

# Or run in detached mode
docker-compose -f docker-compose-dev.yml up -d --build

# View logs
docker-compose -f docker-compose-dev.yml logs -f

# Stop services
docker-compose -f docker-compose-dev.yml down

# Stop services and remove volumes (clean slate)
docker-compose -f docker-compose-dev.yml down -v
```

### 3. Run Database Migrations

The migrations should run automatically. If not, you can run them manually:

```bash
# Execute migrations inside the API container
docker-compose -f docker-compose-dev.yml exec api alembic upgrade head
```

### 4. Access the Application

- API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc

## Development Workflow

### Running Locally (without Docker)

1. Activate your virtual environment:
```bash
source myenv/Scripts/activate  # Windows Git Bash
# or
myenv\Scripts\activate.bat     # Windows CMD
# or
.\myenv\Scripts\Activate.ps1   # Windows PowerShell
```

2. Make sure PostgreSQL is running locally and use `.env` with `DATABASE_HOSTNAME=localhost`

3. Run the app:
```bash
uvicorn app.main:app --reload
```

### Running with Docker Compose

The docker-compose setup:
- Uses hot-reload (changes are reflected immediately)
- Mounts your local code into the container
- Waits for PostgreSQL to be healthy before starting the API
- Persists database data in a Docker volume

## Troubleshooting

### Port Already in Use
If you get an error that port 5432 or 8000 is already in use:

```bash
# Find and stop the process using the port
# On Windows
netstat -ano | findstr :5432
taskkill /PID <PID> /F

# Or change the port in docker-compose-dev.yml
```

### Database Connection Issues
- Ensure `DATABASE_HOSTNAME=postgres` in the docker-compose environment variables
- Check if postgres service is healthy: `docker-compose -f docker-compose-dev.yml ps`

### Clean Start
If you want to start fresh:

```bash
# Remove all containers, networks, and volumes
docker-compose -f docker-compose-dev.yml down -v

# Rebuild and start
docker-compose -f docker-compose-dev.yml up --build
```

## Environment Variables

| Variable | Description | Local Dev | Docker |
|----------|-------------|-----------|--------|
| DATABASE_HOSTNAME | Database host | localhost | postgres |
| DATABASE_PORT | Database port | 5432 | 5432 |
| DATABASE_PASSWORD | Database password | your_password | your_password |
| DATABASE_NAME | Database name | fastapi | fastapi |
| DATABASE_USERNAME | Database user | postgres | postgres |
| SECRET_KEY | JWT secret key | (set your own) | (set your own) |
| ALGORITHM | JWT algorithm | HS256 | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry | 30 | 30 |

## Commands Cheatsheet

```bash
# Build images
docker-compose -f docker-compose-dev.yml build

# Start services
docker-compose -f docker-compose-dev.yml up

# Start in background
docker-compose -f docker-compose-dev.yml up -d

# View logs
docker-compose -f docker-compose-dev.yml logs -f api
docker-compose -f docker-compose-dev.yml logs -f postgres

# Stop services
docker-compose -f docker-compose-dev.yml down

# Execute commands in container
docker-compose -f docker-compose-dev.yml exec api bash
docker-compose -f docker-compose-dev.yml exec postgres psql -U postgres -d fastapi

# Run migrations
docker-compose -f docker-compose-dev.yml exec api alembic upgrade head

# Create new migration
docker-compose -f docker-compose-dev.yml exec api alembic revision --autogenerate -m "description"
```


