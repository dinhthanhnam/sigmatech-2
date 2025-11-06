from i18n import t

class UserNotFoundError(Exception):
    def __init__(self):
        message = t('common.auth.user_not_found')
        super().__init__(message)