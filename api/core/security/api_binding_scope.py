from enum import Enum

class ApiBindingScope(str, Enum):
    PUBLIC = "public"
    BIND_TO_USER = "bind_to_user"
    SUPERUSER_ONLY = "superuser_only"