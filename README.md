# TORCHLITE API
Backend API for the TORCHLITE application.

## Pre-requisites
1. Python 3.11 or higher.
2. MongoDB (an alternative is to connect to an existing deployed MongoDB instance containing relevant data)
3. Redis (an alternative is to connect to an existing deployed Redis instance)
4. Docker is installed and running (optional).

## Local Installation Instructions

1. Create a Python virtual environment
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   poetry lock --no-update
   poetry install
   ```

## Running 

1. Run the application
    ```bash
    poetry run uvicorn htrc.torchlite.app:api --reload --log-config log_conf.yaml
    ```

## Docker Installation Instructions

1. Build the Docker image
    ```bash
    docker build -t torchlite-backend .
    ```
2. Run the Docker container
    ```bash
    docker run -d -p 8000:8000 torchlite-backend
    ```

## API Documentation
Open the API documentation in your browser at http://127.0.0.1:8000/docs.
