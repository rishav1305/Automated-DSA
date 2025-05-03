FROM python:3.11-slim

# Install git and other dependencies
RUN apt-get update && apt-get install -y \
    git \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --upgrade pip setuptools wheel

# Set up working directory
WORKDIR /root

# Install the required Python packages
RUN pip install -r requirements.txt

# Ensure Python outputs are sent straight to terminal
ENV PYTHONUNBUFFERED=1


# Create a directory for user files that will be mounted as a volume
RUN mkdir -p /root/workspace
VOLUME [ "/root/workspace" ]

# Use the entrypoint script
CMD [ "/bin/bash" ]

