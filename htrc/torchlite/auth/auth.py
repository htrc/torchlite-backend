from typing import Annotated

from authlib.integrations.starlette_client import OAuth
from authlib.jose import jwt
from authlib.oidc.core import UserInfo
from fastapi import Depends, HTTPException, status
from fastapi.security import OpenIdConnect

from ..config import config

OIDC_DISCOVERY_URL = f"{config.KEYCLOAK_REALM}/.well-known/openid-configuration"

authlib_oauth = OAuth()
authlib_oauth.register(
    name=config.PROJECT_NAME,
    server_metadata_url=OIDC_DISCOVERY_URL,
    client_id=config.TORCHLITE_CLIENT_ID,
    client_secret=config.TORCHLITE_CLIENT_SECRET,
    client_kwargs={
        "scope": config.TORCHLITE_DEFAULT_SCOPES,
    },
)

fastapi_oauth2 = OpenIdConnect(
    openIdConnectUrl=OIDC_DISCOVERY_URL,
    scheme_name="Keycloak",
    auto_error=False,
)

Token = Annotated[str | None, Depends(fastapi_oauth2)]


async def get_current_user(token: Token) -> UserInfo | None:
    user = None

    if token:
        if token.startswith("Bearer"):
            token = token[7:]

        try:
            jwk = await authlib_oauth.torchlite.fetch_jwk_set()
            claims_options = {
                "azp": {"essential": True, "value": config.PROJECT_NAME},
            }
            claims = jwt.decode(token, jwk, claims_options=claims_options)
            claims.validate(leeway=config.AUTH_LEEWAY)
        except Exception as exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exp),
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            user = UserInfo(claims)

    return user

async def get_user_access_token(token: Token) -> Token | None:
    if token:
        return token
    else:
        return None