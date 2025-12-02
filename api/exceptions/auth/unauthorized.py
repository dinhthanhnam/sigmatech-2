from i18n import t

class UnauthorizedError(Exception):
    def __init__(self):
        message = t('common.auth.unauthorized')
        super().__init__(message)