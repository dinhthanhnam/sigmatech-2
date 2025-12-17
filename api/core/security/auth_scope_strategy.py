from abc import ABC, abstractmethod
from fastapi import Request, HTTPException, status
from models import User
from i18n import t


class AuthScopeStrategy(ABC):
    @abstractmethod
    def check(self, request: Request) -> bool:
        """Kiểm tra scope của route có tương đương với quyền của user không"""
        pass


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
        model = getattr(request.state, "model_to_bind", None) or User
        if not key and model:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("common.auth.forbidden"),
            )
        path = {}
        path["id"] = request.path_params.get("id", None)
        condition = [getattr(model, str(key)) == state_user.id]
        if path["id"] and model != User:
            condition.append(model.id == int(path["id"]))
        related = model.query().where(*condition).first()
        if not related:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=t("common.auth.forbidden"),
            )
        return True
