#!/bin/bash
# Stop any running containers with the same name
docker stop community-connect || true
docker rm community-connect || true

# Run the new container
docker run -d --name community-connect -p 8000:8000 \
  -e RDS_DB_NAME=$RDS_DB_NAME \
  -e RDS_USERNAME=$RDS_USERNAME \
  -e RDS_PASSWORD=$RDS_PASSWORD \
  -e RDS_HOSTNAME=$RDS_HOSTNAME \
  $DOCKER_USERNAME/community-connect:latest
