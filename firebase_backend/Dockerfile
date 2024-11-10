# Use an official Python runtime as the base image
FROM --platform=linux/amd64 python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Flask to run on
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
