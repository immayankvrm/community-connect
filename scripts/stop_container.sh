#!/bin/bash
# Stop the existing Docker container
docker stop community-connect || true
docker rm community-connect || true
