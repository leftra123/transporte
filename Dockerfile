# Use the official Python image as base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Run the command to start the app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "colegio_transportes.wsgi:application"]
