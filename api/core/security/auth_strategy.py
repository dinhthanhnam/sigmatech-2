from abc import ABC, abstractmethod
from fastapi import Request
from models import User
from utils.jwt import decode_token


class AuthStrategy(ABC):
    @abstractmethod
    def can_handle(self, request: Request) -> bool:
        """Kiểm tra request có chứa credential phù hợp với strategy không"""
        pass

    @abstractmethod
    def authenticate(self, request: Request) -> User | None:
        """Thực hiện xác thực"""
        pass


class ApiKeyAuthStrategy(AuthStrategy):
    def can_handle(self, request: Request) -> bool:
        return True if request.headers.get("x-api-key") else False

    def authenticate(self, request: Request) -> User | None:
        user = User.find_by_username("nextserver")
        request.state.user = user
        return user


class TokenBearerAuthStrategy(AuthStrategy):
    def can_handle(self, request: Request) -> bool:
        auth_header = request.headers.get("Authorization", "")
        return auth_header.startswith("Bearer ")

    def authenticate(self, request: Request) -> User | None:
        token = request.headers["Authorization"].split(" ", 1)[1]
        decoded = decode_token(token)
        user = User.find_by_id(int(decoded["sub"]))
        request.state.user = user
        return user