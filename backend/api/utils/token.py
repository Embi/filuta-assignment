import jwt
from api.utils.conf import ApiSettings

__TOKEN_ALGORITHM = ApiSettings().token_algorithm
__TOKEN_SECRET = ApiSettings().token_secret


def encode(payload: dict) -> str:
    return jwt.encode(payload, __TOKEN_SECRET, algorithm=__TOKEN_ALGORITHM)


def decode(token: str) -> dict:
    return jwt.decode(token, __TOKEN_SECRET, algorithms=[__TOKEN_ALGORITHM])
