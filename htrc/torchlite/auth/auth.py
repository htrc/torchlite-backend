from typing import Annotated

from authlib.integrations.starlette_client import OAuth
from authlib.jose import jwt
from authlib.oidc.core import UserInfo
from fastapi import Depends, HTTPException
from fastapi.security import OpenIdConnect
from starlette import status

from ..config import Config

OIDC_DISCOVERY_URL = f"{Config.KEYCLOAK_REALM}/.well-known/openid-configuration"

authlib_oauth = OAuth()
authlib_oauth.register(
    name=Config.PROJECT_NAME,
    server_metadata_url=OIDC_DISCOVERY_URL,
    client_id=Config.TORCHLITE_CLIENT_ID,
    client_secret=Config.TORCHLITE_CLIENT_SECRET,
    client_kwargs={
        "scope": Config.TORCHLITE_DEFAULT_SCOPES,
    },
)

fastapi_oauth2 = OpenIdConnect(
    openIdConnectUrl=OIDC_DISCOVERY_URL,
    scheme_name="Keycloak",
    auto_error=False,
)


async def get_current_user(token: Annotated[str | None, Depends(fastapi_oauth2)]) -> UserInfo | None:
    user = None

    if token:
        if token.startswith("Bearer"):
            token = token[7:]

        try:
            jwk = await authlib_oauth.torchlite.fetch_jwk_set()
            claims_options = {
                "azp": {"essential": True, "value": Config.PROJECT_NAME},
            }
            claims = jwt.decode(token, jwk, claims_options=claims_options)
            claims.validate(leeway=11120)
        except Exception as exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exp),
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            user = UserInfo(claims)

    return user
