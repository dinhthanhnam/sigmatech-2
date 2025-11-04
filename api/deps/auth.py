from fastapi.security import HTTPBearer, APIKeyHeader
from fastapi import Depends


authorization_header = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

auth_deps = (Depends(authorization_header), Depends(api_key_header))

