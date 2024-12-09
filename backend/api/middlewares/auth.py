from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request


class FakeAuthMiddleware(BaseHTTPMiddleware):
    """
    This Middleware doesn't really do any authentification or validation
    of token info. It basically just decodes the token, extracts user email
    and query User object from database.

    Assuming a standalone OIDC server exists, this middleware would
    """

    def __init__(self, app: FastAPI, F, token_secret: str):
        super().__init__(app)
        self.token_secret = token_secret

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response
