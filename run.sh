#!/usr/bin/env bash
set -euo pipefail

IMAGE="recipe-mcp"
CONTAINER="recipe-mcp-server"
PORT=8002

# Stop and remove any existing container
docker stop "$CONTAINER" 2>/dev/null || true
docker rm "$CONTAINER" 2>/dev/null || true

# Rebuild the image
echo "Building $IMAGE ..."
docker build -t "$IMAGE" .

# Run with a named volume for persistent recipe storage
echo "Starting $CONTAINER on port $PORT ..."
docker run -d \
  --name "$CONTAINER" \
  --restart unless-stopped \
  -p "$PORT:8000" \
  -v recipe-data:/data \
  "$IMAGE"

echo "Done. Open http://localhost:$PORT"
