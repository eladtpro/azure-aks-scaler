# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Create a virtual environment and activate it
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN . /opt/venv/bin/activate

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --upgrade pip -r requirements.txt

# Define environment variable
# ENV SUBSCRIPTION
# ENV NODE_POOLS_AMOUNT={ "manualpool2": 5, "manualpool3": 5 }
# ENV RESOURCE_GROUP
# ENV CLUSTER_NAME

# Run main.py when the container launches
CMD ["python", "main.py"]