import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from src.api.auth import auth_required
from src.api.schemas.twitter import (
    TwitterAccessTokenRequest,
    TwitterAuthUrlResponse,
    TwitterIsAuthenticatedResponse,
)
from src.dependencies import TwitterServiceClient
from src.services.user_service.types import User

router = APIRouter()


@router.post("/twitter/auth-url", response_model=TwitterAuthUrlResponse)
async def generate_twitter_auth_url(twitter_service: TwitterServiceClient):
    try:
        auth_url = twitter_service.get_auth_url()
        return TwitterAuthUrlResponse(auth_url=auth_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/twitter/access-token")
async def sets_twitter_access_token(
    user: Annotated[User, Depends(auth_required)],
    request: TwitterAccessTokenRequest,
    twitter_service: TwitterServiceClient,
):
    try:
        access_token = twitter_service.set_access_token(
            user.id, request.auth_response_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/twitter/is-authenticated")
async def is_twitter_authenticated(
    user: Annotated[User, Depends(auth_required)],
    twitter_service: TwitterServiceClient,
):
    return TwitterIsAuthenticatedResponse(
        is_authenticated=twitter_service.is_twitter_authenticated(user.id)
    )
