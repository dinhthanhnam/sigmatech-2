from i18n import t

class UnauthorizedError(Exception):
    def __init__(self):
        message = t('common.auth.forbidden')
        super().__init__(message)