# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Avoid timezone prompt during installations
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    ln -s /usr/bin/python3 /usr/bin/python

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME MarketVisor

# Set the ENTRYPOINT to Python interpreter and script
ENTRYPOINT ["python", "main.py"]
