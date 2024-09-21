#!/bin/bash
# Update the package index
sudo apt-get update

# Install Docker if it's not installed
if ! [ -x "$(command -v docker)" ]; then
  sudo apt-get install -y docker.io
  sudo systemctl start docker
  sudo systemctl enable docker
fi
