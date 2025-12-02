from enum import Enum
from exceptions import UnauthorizedError
from models import User
from core.config import settings
from utils.jwt import decode_token
from fastapi import Depends, Request, HTTPException, status
from i18n import t


class AuthType(str, Enum):
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"


class AuthStrategy:
    def __init__(self, auth_type: AuthType):
        self.auth_type = auth_type

    def authenticate(self, credential, request: Request) -> bool:
        if self.auth_type == AuthType.API_KEY:
            user = User.find_by_username("nextserver")
            request.state.user = user
            print(user)
            return True
        elif self.auth_type == AuthType.BEARER_TOKEN:
            decoded = decode_token(credential)
            user = User.find_by_id(int(decoded["sub"]))
            request.state.user = user
            print(user)
            return user is not None


# Extract credential helper
def get_credential(request: Request):
    auth_header = request.headers.get("Authorization")
    api_key_header = request.headers.get("x-api-key")

    if api_key_header:
        return api_key_header
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1]

    return None


class AuthManager:
    def __call__(self, request: Request) -> bool:
        """Credential can be either an API key or a bearer token"""
        credential = get_credential(request)
        print("Credential:", credential)
        if not credential:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=t('common.auth.unauthorized')
            )
        strategy = AuthStrategy(AuthType.API_KEY) if credential == settings.service_secret else AuthStrategy(AuthType.BEARER_TOKEN)
        if not strategy.authenticate(credential, request):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=t('common.auth.unauthorized')
            )
        
        return self

