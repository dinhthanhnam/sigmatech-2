from i18n import t

class PasswordMismatchedError(Exception):
    def __init__(self):
        message = t('common.auth.password_mismatched')
        super().__init__(message)