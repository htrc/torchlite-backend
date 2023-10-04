import os
from dataclasses import dataclass

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
    AUTH_LEEWAY = 11120

    TORCHLITE_UID = "95164779-1fc9-4592-9c74-7a014407f46d"


config = Config
