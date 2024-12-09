from fastapi import APIRouter
from fastapi import Depends
from api.utils.auth import authenticate
from api.validation.users import UserResponse

router = APIRouter()


# @router.get("")
# async def list_users(user: dict = Depends(authenticate)):
# """List all users."""
# # TODO
# return user


@router.get("/me")
async def get_user_details(user: dict = Depends(authenticate)) -> UserResponse:
    """Get details about the authenticated user."""
    return UserResponse(**user.to_dict())


# TODO Ask customer for his preferences via a questionnaire
# @router.post("/questionnaire")
# async def search(
# user: dict = Depends(authenticate)
# ):
# """Sumbit preference questionnare for the authenticated user."""
# return user
