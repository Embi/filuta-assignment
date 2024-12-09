from pydantic import BaseModel


class FakeTokenRequest(BaseModel):
    email: str = "john1@example.com"


class FakeTokenResponse(BaseModel):
    token: str
