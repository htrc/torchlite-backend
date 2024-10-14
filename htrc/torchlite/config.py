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
    REGISTRY_API_URL = os.environ.get("REGISTRY_API_URL", "https://analytics.dev.htrc.indiana.edu")
    FEATURED_WORKSET_USER = os.environ.get("FEATURED_WORKSET_USER")
    FEATURED_WORKSETS_URL = os.environ.get("FEATURED_WORKSETS_URL")

    # Cache settings
    ENABLE_CACHE = os.environ.get("ENABLE_CACHE", "false").lower() == "true"
    CACHE_EXPIRE = int(os.environ.get("CACHE_EXPIRE", "300"))
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
    REDIS_DB = int(os.environ.get("REDIS_DB", "1"))
    REDIS_PREFIX = os.environ.get("REDIS_PREFIX", "torchlite-cache")
    CACHE_STATUS_HEADER = "x-torchlite-cache"


config = Config
