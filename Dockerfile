# Use an official Python runtime as a parent image with better compatibility
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies for uWSGI
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpcre3 \
    libpcre3-dev \
    libssl-dev \
    && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .


# Collect static files
RUM mkdir static
RUN python manage.py collectstatic --noinput

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=oms.settings
ENV PYTHONUNBUFFERED=1

# Expose ports for gRPC and Django services
EXPOSE 50057 50058 50059 8001

# Create an entrypoint script to run both the Django server and the gRPC service
RUN echo '#!/bin/sh\n\
python manage.py makemigrations && \
python manage.py migrate && \
uwsgi --http :8001 --module oms.wsgi:application --master --processes 4 --threads 2 & \
python server.py' > /usr/src/app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/src/app/entrypoint.sh

# Set the entrypoint to run the script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
