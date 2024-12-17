# TORCHLITE API
Backend API for the TORCHLITE application.

## Pre-requisites
1. Python 3.11 or higher.
2. MongoDB (an alternative is to connect to an existing deployed MongoDB instance containing relevant data)
3. Redis (an alternative is to connect to an existing deployed Redis instance)
4. Docker is installed and running (recommended).

## Install Dependencies

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

## Environment Variables

Create a `.env` file in the root directory and add the following environment variables, and replace the placeholders with the actual values:

```bash
KEYCLOAK_REALM=<realm>
TORCHLITE_CLIENT_ID=<keycloak_client_id>
TORCHLITE_CLIENT_SECRET=<ckeycloak_lient_secret>
FEATURED_WORKSETS_URL=<url>
MONGODB_URL=<mongodb_url>
REDIS_HOST=<redis_host>
ENABLE_CACHE=<True/False>
CACHE_EXPIRE=<cache_expiration_time_in_seconds>
REGISTRY_API_URL=<registry_api_url>
FEATURED_WORKSET_USER=<featured_workset_user>
```

## Running the API using Docker Container (Recommended)

1. Build the Docker image
    ```bash
    docker buildx build --no-cache -t torchlite-backend .
    ```
2. Run the TORCHLITE Backend using EITHER of the steps below.
   
   a. Using Docker Run command. This assumes that MongoDB and Redis are running on the host machine.
    ```bash
    docker run --env-file .env -p 8000:8000 torchlite-backend
    ```
   b. Using Docker Compose (further testing and updating the instructions may be needed)
    ```bash
    docker-compose up
    ```

## Running the API using Poetry (Alternative) 

1. Run the application
    ```bash
    poetry run uvicorn htrc.torchlite.app:api --reload --log-config log_conf.yaml
    ```

## API Documentation
Open the API documentation in your browser at http://127.0.0.1:8000/docs.
