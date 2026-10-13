# !/bin/bash
# Block 1 — Image Management
# Step 3: Clean up images and containers

echo "========================================"
echo "  Removing stopped containers"
echo "========================================"
docker container prune -f
docker container rm <container-ID>

echo ""
echo "========================================"
echo "  Removing hello-world image"
echo "========================================"
docker rmi hello-world
docker rmi <Image-ID>

echo ""
echo "========================================"
echo "  Remaining images"
echo "========================================"
docker images

echo ""
echo "Cleanup complete."
