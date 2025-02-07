# Use an official Python runtime as a parent image with better compatibility
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies for uWSGI and Supervisor
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpcre3 \
    libpcre3-dev \
    libssl-dev \
    supervisor \
    && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Collect static files
RUN mkdir static
RUN python manage.py collectstatic --noinput

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=oms.settings
ENV PYTHONUNBUFFERED=1

# Expose ports for gRPC, Django services, and any other services
EXPOSE 50057 50058 50059 8001

# Copy the Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set the entrypoint to run Supervisor
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
