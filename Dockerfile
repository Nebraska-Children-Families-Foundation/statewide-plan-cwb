# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Copy the entrypoint script into the container at /entrypoint.sh
COPY entrypoint.sh /entrypoint.sh

# Grant permissions to execute the entrypoint script
RUN chmod +x /entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["/entrypoint.sh"]

# Set environment variable for Django
ENV DJANGO_ENV=production

# Expose port 8000
EXPOSE 8000

# Set the command to run your application
CMD ["gunicorn", "statewideplanCWB.wsgi:application", "--bind", "0.0.0.0:8000"]
