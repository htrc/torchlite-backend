# TORCHLITE API
Backend API for the TORCHLITE application.

## Pre-requisites
1. Python 3.11 or higher.
2. MongoDB (an alternative is to connect to an existing deployed MongoDB instance containing relevant data)
3. Docker is installed and running (optional).


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
    docker build -t torchlite-api .
    ```
2. Run the Docker container
    ```bash
    docker run -d -p 8000:8000 torchlite-api
    ```

## API Documentation
Open the API documentation in your browser
    ```
    http://127.0.0.1:8000/docs
