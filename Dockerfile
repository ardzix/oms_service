# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=oms.settings
ENV PYTHONUNBUFFERED=1

# Collect static files
# RUN python manage.py collectstatic --noinput

# Expose port for gRPC
EXPOSE 50057 50058

# Run the command to start uWSGI
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python server.py"]
