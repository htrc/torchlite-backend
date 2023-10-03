import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    PROJECT_NAME = "torchlite"
    LOCAL_DEV = os.environ.get("ENV", "dev") == "dev"

    DB_USER = os.environ.get("DB_USER", "torchlite")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "torchlite")
    DB_NAME = os.environ.get("DB_NAME", PROJECT_NAME)
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    KEYCLOAK_REALM = os.environ["KEYCLOAK_REALM"]
    TORCHLITE_CLIENT_ID = os.environ["TORCHLITE_CLIENT_ID"]
    TORCHLITE_CLIENT_SECRET = os.environ["TORCHLITE_CLIENT_SECRET"]
    TORCHLITE_DEFAULT_SCOPES = "openid email profile offline_access"
