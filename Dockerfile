# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Set the command to run your application
ENV DJANGO_ENV=production
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
