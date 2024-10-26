from pydantic import BaseModel


class TwitterAccessTokenRequest(BaseModel):
    auth_response_url: str


class TwitterAuthUrlResponse(BaseModel):
    auth_url: str


class TwitterIsAuthenticatedResponse(BaseModel):
    is_authenticated: bool
