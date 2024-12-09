from pydantic import BaseModel


class UserResponse(BaseModel):
    email: str = "john1@example.com"
    first_name: str = "John1"
    surname: str = "Doe"
