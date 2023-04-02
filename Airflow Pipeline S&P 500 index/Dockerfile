# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Set environment variables
ENV AIRFLOW_HOME=/app/airflow
ENV PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"

# Expose the port that Airflow webserver will run on
EXPOSE 8080

# Start the Airflow webserver and scheduler
CMD ["airflow", "webserver", "-p", "8080"]
CMD ["airflow", "scheduler"]
