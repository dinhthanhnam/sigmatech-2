from fastapi.security import HTTPBearer, APIKeyHeader, OAuth2PasswordBearer
from fastapi import Depends


# Define security schemes
authorization_header = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
password_bearer = OAuth2PasswordBearer("auth/login/form", auto_error=False)

auth_deps = (Depends(authorization_header), Depends(api_key_header), Depends(password_bearer))

