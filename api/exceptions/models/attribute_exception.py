class AttributeNotFoundError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Attribute '{name}' not found.")
        self.name = name