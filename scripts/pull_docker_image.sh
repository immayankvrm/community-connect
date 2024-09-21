#!/bin/bash
# Login to Docker Hub
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

# Pull the latest version of the Docker image from Docker Hub
docker pull $DOCKER_USERNAME/community-connect:latest
