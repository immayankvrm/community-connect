# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/
# RUN apt-get update && sudo apt-get install python3-dev default-libmysqlclient-dev
# Install dependencies

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && apt-get clean \
RUN pip install mysqlclient
RUN pip install -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
