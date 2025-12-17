from typing import Type, TypeVar, Optional, Literal
from models.base import Base
from models.user import User
from fastapi import Request, HTTPException, status
from i18n import t
from .api_binding_scope import ApiBindingScope
from .auth_strategy import AuthStrategy, ApiKeyAuthStrategy, TokenBearerAuthStrategy
from .auth_scope_strategy import AuthScopeStrategy, PublicAuthScopeStrategy, SuperuserOnlyAuthScopeStrategy, BindToUserAuthScopeStrategy

T = TypeVar("T", bound=Base)

class AuthManager:
    def __init__(self, scope: ApiBindingScope, model_to_bind: Optional[Type[T]] = None, key_to_bind: Literal["user_id" , "author_id", "id"] = "id"):
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
        self.check_scope(request)

        return self

    def authenticate_with_strategies(self, request: Request) -> User | None:
        for strategy in self.auth_strategies:
            if strategy.can_handle(request):
                return strategy.authenticate(request)
        return None

    def check_scope(self, request: Request):
        strategy: AuthScopeStrategy = self.scope_strategies[self.scope]
        strategy.check(request)
