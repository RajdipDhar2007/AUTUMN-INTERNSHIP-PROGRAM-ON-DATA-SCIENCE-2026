#!/bin/bash
# Block 1 — Image Management
# Step 2: List images and run a container

echo "========================================"
echo "  All locally available Docker images"
echo "========================================"
docker images

echo ""
echo "========================================"
echo "  Running hello-world container"
echo "========================================"
docker run hello-world

echo ""
echo "========================================"
echo "  Containers currently running (ps)"
echo "========================================"
docker ps
docker container ls

echo ""
echo "========================================"
echo "  All containers (including stopped)"
echo "========================================"
docker ps -a
docker container ls -a

# Note
# - `docker ps`` is the shorter, traditional command.
# - `docker container ls` is the more explicit form in Docker's command structure.
# Both are valid and produce equivalent results.