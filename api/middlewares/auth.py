from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from utils.jwt import decode_token
from models import User
from deps import authorization_header

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(authorization_header)
):
    token = credentials.credentials
    payload = decode_token(token)
    user = User.find_by_id(payload["sub"])
    return user