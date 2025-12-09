from abc import ABC, abstractmethod
from enum import Enum
from exceptions import UnauthorizedError
from models import User
from core.config import settings
from utils.jwt import decode_token
from fastapi import Depends, Request, HTTPException, status
from i18n import t
from typing import Literal, Type, TypeVar
from models.base import Base


T = TypeVar("T", bound=Base)


class AuthType(str, Enum):
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"


class ApiBindingScope(str, Enum):
    PUBLIC = "public"
    BIND_TO_USER = "bind_to_user"
    SUPERUSER_ONLY = "superuser_only"


class AuthStrategy(ABC):
    @abstractmethod
    def can_handle(self, request: Request) -> bool:
        """Kiểm tra request có chứa credential phù hợp với strategy không"""
        pass

    @abstractmethod
    def authenticate(self, request: Request) -> User | None:
        """Thực hiện xác thực"""
        pass


class AuthScopeStrategy(ABC):
    @abstractmethod
    def check(self, request: Request) -> bool:
        """Kiểm tra scope của route có tương đương với quyền của user không"""
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
        print("User state after authenticate", request.state.user)
        return user


class PublicAuthScopeStrategy(AuthScopeStrategy):
    def check(self, request: Request) -> bool:
        return True


class SuperuserOnlyAuthScopeStrategy(AuthScopeStrategy):
    def check(self, request: Request) -> bool:
        user: User = request.state.user
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("common.auth.forbidden"),
            )
        return True


class BindToUserAuthScopeStrategy(AuthScopeStrategy):
    def check(self, request: Request) -> bool:
        state_user: User = request.state.user
        #Superuser luôn có quyền truy cập
        if state_user.is_superuser:
            return True
        key = getattr(request.state, "key_to_bind", None)
        model: Type[T] = getattr(request.state, "model_to_bind", None) or User
        if not key and model:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("common.auth.forbidden"),
            )
        path = {}
        path["id"] = request.path_params.get("id", None)
        condition = [getattr(model, key) == state_user.id]
        if path["id"] and model != User:
            condition.append(model.id == int(path["id"]))
        related = model.query().where(*condition).first()
        if not related:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("common.auth.forbidden"),
            )
        print("Related", related)
        return True


class AuthManager:
    def __init__(self, scope: ApiBindingScope, model_to_bind: Type[T] = None, key_to_bind: Literal["user_id" , "author_id", "id"] = "id"):
        """
        params:
            scope: Phạm vi xác thực
            model_to_bind: Model để ràng buộc (mặc định là User)
            key_to_bind: Khóa để ràng buộc (mặc định là 'id')
        """
        self.scope: ApiBindingScope = scope
        self.auth_strategies: list[AuthStrategy] = [
            ApiKeyAuthStrategy(),
            TokenBearerAuthStrategy(),
        ]
        self.scope_strategies = {
            ApiBindingScope.PUBLIC: PublicAuthScopeStrategy(),
            ApiBindingScope.SUPERUSER_ONLY: SuperuserOnlyAuthScopeStrategy(),
            ApiBindingScope.BIND_TO_USER: BindToUserAuthScopeStrategy(),
        }
        self.user: User | None = None
        self.key_to_bind = key_to_bind
        self.model_to_bind = model_to_bind

    def __call__(self, request: Request):
        request.state.key_to_bind = self.key_to_bind
        request.state.model_to_bind = self.model_to_bind

        user = self.authenticate_with_strategies(request)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=t("common.auth.unauthorized"),
            )
        
        self.user = user
        print("Before check scope")
        self.check_scope(request)
        print("After check scope",self.check_scope(request))

        return self

    def authenticate_with_strategies(self, request: Request) -> User | None:
        print("Before authenticate:", getattr(request.state, "user", None))
        for strategy in self.auth_strategies:
            if strategy.can_handle(request):
                return strategy.authenticate(request)
        return None

    def check_scope(self, request: Request):
        strategy: AuthScopeStrategy = self.scope_strategies[self.scope]
        strategy.check(request)


