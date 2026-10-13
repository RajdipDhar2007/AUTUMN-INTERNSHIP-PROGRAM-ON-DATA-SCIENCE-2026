#!/bin/bash
# Block 1 — Image Management
# Step 1: Pull images from Docker Hub

echo "========================================"
echo "  Pulling images from Docker Hub"
echo "========================================"

echo ""
echo ">>> Pulling python:3.11-slim ..."
docker pull python:3.11-slim

echo ""
echo ">>> Pulling hello-world ..."
docker pull hello-world

echo ""
echo "========================================"
echo "  Done! Run 02_list_and_run.sh next."
echo "========================================"
