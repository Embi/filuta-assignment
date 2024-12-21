from pydantic import BaseModel


class FakeTokenRequest(BaseModel):
    email: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john1@example.com",
                }
            ]
        }
    }


class FakeTokenResponse(BaseModel):
    token: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "token": "SOMEJWTTOKEN",
                }
            ]
        }
    }
