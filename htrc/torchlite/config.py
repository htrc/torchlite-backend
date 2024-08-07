import os
from dataclasses import dataclass
from uuid import UUID

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    PROJECT_NAME = "torchlite"
    LOCAL_DEV = os.environ.get("ENV", "dev") == "dev"

    MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017/torchlite")

    KEYCLOAK_REALM = os.environ["KEYCLOAK_REALM"]
    TORCHLITE_CLIENT_ID = os.environ["TORCHLITE_CLIENT_ID"]
    TORCHLITE_CLIENT_SECRET = os.environ["TORCHLITE_CLIENT_SECRET"]
    TORCHLITE_DEFAULT_SCOPES = "openid email profile offline_access"
    AUTH_LEEWAY = int(os.environ.get("AUTH_LEEWAY_SECONDS", "120"))  # seconds

    TORCHLITE_UID = UUID("95164779-1fc9-4592-9c74-7a014407f46d")  # do not change
    EF_API_URL = os.environ.get("EF_API_URL", "https://data.htrc.illinois.edu/ef-api")
    REGISTRY_API_URL = os.environ.get("REGISTRY_API_URL")
    FEATURED_WORKSET_USER = os.environ.get("FEATURED_WORKSET_USER")

    FEATURED_WORKSETS_URL = os.environ.get("FEATURED_WORKSETS_URL")


config = Config
