from fastapi import APIRouter
from src.api.schemas.users import CreateUserRequest
from src.dependencies import UserServiceClient

router = APIRouter()


@router.post("/users")
async def sign_in_user(
    create_user_request: CreateUserRequest, user_service: UserServiceClient
):
    user_service.create_user(
        email=create_user_request.email,
        name=create_user_request.name,
        clerk_id=create_user_request.clerk_id,
        sign_in_method=create_user_request.sign_in_method,
    )
