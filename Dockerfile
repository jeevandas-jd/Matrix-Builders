# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project to the container
COPY . /app/

# Run migrations and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the Django app with gunicorn in production
CMD ["gunicorn", "babylon.wsgi:application", "--bind", "0.0.0.0:8000"]
