from api.utils.token import encode
from fastapi import APIRouter
from api.validation.token import FakeTokenRequest, FakeTokenResponse

router = APIRouter()


@router.post("/fake-token")
async def get_fake_token(body: FakeTokenRequest) -> FakeTokenResponse:
    """Generate a fake jwt token for given email."""
    return FakeTokenResponse(token=encode(body.dict()))
