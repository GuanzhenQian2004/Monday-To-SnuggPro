# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /webhook-app

# Copy the current directory contents into the container at /app
COPY . /webhook-app

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "-m", "app.app"]
