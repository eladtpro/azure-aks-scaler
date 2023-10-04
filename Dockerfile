# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Create a virtual environment and activate it
RUN python -m venv /.venv
ENV PATH="/.venv/bin:$PATH"
RUN . /.venv/bin/activate

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --upgrade pip -r requirements.txt

# Define environment variable
# ENV SUBSCRIPTION_ID
# ENV NODE_POOLS_AMOUNT={ "manualpool2": 5, "manualpool3": 5 }
# ENV RESOURCE_GROUP
# ENV CLUSTER_NAME
# ENV AZURE_TENANT_ID=xxx
# ENV AZURE_CLIENT_ID=xxx
# ENV AZURE_CLIENT_SECRET=xxx
# ENV SUBSCRIPTION_ID=xxx

# Run main.py when the container launches
# CMD ["python", "app/main.py"]

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

EXPOSE 5000
# Run the Flask application when the container launches
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["python", "app/app.py", "--host=0.0.0.0"]