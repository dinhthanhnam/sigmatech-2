class AttributeNotFoundError(Exception):
    def __init__(self, name: str):
        message = f"Attribute '{name}' not found."
        super().__init__(message)
        self.name = name