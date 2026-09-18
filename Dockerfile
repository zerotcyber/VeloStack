# Production grade Dockerfile for my fastAPI app

# Builder stage
# Define the base image
FROM python:3.12.3-slim-bookworm AS builder
# Set working directory
WORKDIR /app
# Copy dependencies first to leverage layer caching and minimize build time
COPY requirements.txt .
# Install python packages
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt



# Runtime Stage
FROM python:3.12.3-slim-bookworm AS runner
# Declare Environment variables
ENV PATH="/install/bin:${PATH}" \
    PYTHONPATH="/install/lib/python3.12/site-packages" \
    ENVIRONMENT=production \
    APP_PORT=8000
# Working directory
WORKDIR /app

# Create a non-root user and group for security
RUN groupadd -g 10001 appgroup && \
    useradd -r -M -u 10001 -g appgroup -s /sbin/nologin appuser

# Copy the installed dependencies from builder
COPY --from=builder /install /install

# Copy the application source code
COPY app/ ./app/

# Change ownwership of /app to non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose port for documentation
EXPOSE 8000

# Define the startup command
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "2", "app.main:app"]

