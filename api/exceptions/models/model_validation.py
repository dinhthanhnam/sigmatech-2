class ModelValidationError(Exception):
    def __init__(self):
        message = "Model validation failed: instance is None."
        super().__init__(message)