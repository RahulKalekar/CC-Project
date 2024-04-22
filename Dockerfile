# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mount a volume for persistent storage
VOLUME /data

# Run backup_script.py when the container launches
CMD ["python", "backup_script.py"]
