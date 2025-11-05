class UniqueConstraintError(Exception):
    def __init__(self, msg: str):
        if "Duplicate entry" in msg:
            self.value = msg.split("Duplicate entry '")[1].split("'")[0]
            self.field = msg.split("for key '")[1].split("'")[0]
            self.message = f"Duplicate entry '{self.value}' for field '{self.field}'"
        else:
            self.message = "Unique constraint violation"
        super().__init__(msg)