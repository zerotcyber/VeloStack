Task Management API
    
A small REST API for creating and managing tasks, built with FastAPI, SQLAlchemy 2.0 and Pydantic v2.
I built this to practise containerising a real Python service properly: a multi-stage Docker build, a non-root user inside the container, dependency layers for caching, and ahealth check system. The API itself is deliberately simple so the Docker and deployment work stays the focus.
________________________________________
The app is split into four layers, each with one job:
Layer	What it does
API (app/api/)	Handles HTTP requests and responses
Services (app/services/)	Business rules and validation
Repositories (app/repositories/)	All database queries live here
Schemas (app/schemas/)	Pydantic models that define what goes in and out
Keeping database code out of the route handlers means I can change how data is stored without touching the API surface.
What runs inside the container
Gunicorn starts as PID 1 and manages two Uvicorn workers, which handle the async requests. Docker polls GET /health to decide whether the container is actually working, not just running.
Port 8000
   |
   v
Gunicorn (PID 1, user: appuser)
   |-- Uvicorn worker 1
   |-- Uvicorn worker 2
   |
   v
Health check: GET /health
Docker decisions worth explaining
Multi-stage build. The first stage installs dependencies and packages to compile Python wheels. The final stage copies only the finished wheels, so the build tools never ship in the image. The result is a much smaller container.
Runs as a non-root user. The image creates appuser (UID 10001) and runs the app as that user. If someone breaks into the process, they land as an unprivileged user rather than root.
Pinned base image. python:3.12.3-slim-bookworm rather than python:3.12.3, so the image builds the same way on my laptop as it does in CI six months from now.
Dependencies copied before source code. requirements.txt is copied and installed before COPY app/. Editing application code then rebuilds in seconds instead of reinstalling every dependency.
Exec-form CMD. CMD ["gunicorn", ...] rather than CMD gunicorn ..., so Gunicorn is PID 1 and receives SIGTERM directly. Workers shut down gracefully instead of being killed.
Project structure
devops-project-1/
├── app/
│   ├── api/v1/tasks.py       # Routes
│   ├── core/config.py        # Settings loaded from environment
│   ├── core/logging.py       # Logging setup
│   ├── db/session.py         # Database engine and connection pool
│   ├── models/task.py        # SQLAlchemy table definition
│   ├── repositories/task_repo.py
│   ├── schemas/task.py       # Request/response models
│   ├── services/task_service.py
│   └── main.py               # App entrypoint
├── .dockerignore
├── .env.example
├── compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt
Getting started
You'll need Docker 29.0 or newer. Python 3.12+ is optional, only if you want to run the app outside a container.
1. Clone and set up your environment file
git clone https://github.com/your-username/devops-project-1.git
cd devops-project-1
cp .env.example .env
2. Build and run
docker compose up -d --build
Check that it started:
docker compose ps
Without Compose
docker buildx build –t velostack:v1

docker run -d \
  --name velostack-container \
  -p 8000:8000 \
  --env-file .env \
  velostack:1.0.0
Using the API
Interactive docs are generated automatically:
•	Swagger UI: http://localhost:8000/docs
•	ReDoc: http://localhost:8000/redoc
Health check
curl http://localhost:8000/health
{
  "status": "healthy",
  "environment": "development"
}
Create a task
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Verify multi-stage build", "description": "Check the container runs as a non-root user."}'

Observations:
Layer order is the whole game. Moving dependency installation above COPY app/ ./app/ cut rebuild times dramatically, because editing a route no longer invalidates the pip install layer.
Shell form breaks signal handling. With CMD gunicorn ..., the app runs under /bin/sh -c and SIGTERM never reaches Gunicorn, so docker stop waits the full timeout then kills it. Exec form fixed it.
Configuration belongs in the environment. pydantic-settings reads everything from environment variables, so no credentials end up in the code and .env stays out of version control.
Root is the default, not the right choice. Adding a dedicated user and group took three lines in the Dockerfile and removes an entire class of risk.


