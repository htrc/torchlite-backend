# torchlite-backend
Backend API service for Torchlite web dashboard

## Prerequisites
  * Python 3.11+
  * Poetry 1.3.2+
## Installation
  * gh repo clone htrc/torchlite-backend
  * cd torchlite-backend
  * poetry install
## Running the Backend in Development
  * cd src/backend
  * poetry run uvicorn main:tlapi --reload
  
  Point your browser at <http://localhost:8000/docs,> and use the UI to select a workset and add MetadataWidget to the default dashboard
