from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

# from core.db.session import get_db
from core.db.models.user import User
from core.db.session import get_async_session
from sqlalchemy import select
import jwt

from api.utils.token import decode

security = HTTPBearer()


async def authenticate(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> User:
    """Verify token and return corresponding User object."""
    try:
        payload = decode(credentials.credentials)
        user = await get_user(payload["email"])
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def get_user(email: str) -> User:
    # TODO refactor to some db CRUD module
    async with get_async_session() as session:
        statement = select(User).where(User.email == email)
        rows = await session.execute(statement)
        row = rows.first()
        return row[0]
