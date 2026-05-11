from pydantic import BaseModel, field_validator
import re


class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")

        if len(value) > 72:
            raise ValueError("Password must be at most 72 characters")

        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain letters")

        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain numbers")

        return value