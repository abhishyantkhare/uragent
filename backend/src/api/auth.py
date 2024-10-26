import os

import jwt
import requests
from dotenv import load_dotenv
from fastapi import Header, HTTPException
from jwt.algorithms import RSAAlgorithm
from src.dependencies import UserServiceClient

load_dotenv()


def auth_required(
    user_service: UserServiceClient, authorization: str = Header(...)
) -> str:
    """
    returns user if valid
    raises AuthenticationException otherwise
    """
    try:
        token = authorization.split(" ")[1]
    except (AttributeError, KeyError):
        raise HTTPException(status_code=401, detail="No authentication token provided")

    jwks = requests.get(
        "https://api.clerk.com/v1/jwks",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv('CLERK_SECRET_KEY')}",
        },
    ).json()
    public_key = RSAAlgorithm.from_jwk(jwks["keys"][0])
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_signature": True},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Token decode error.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    user_id = payload.get("sub")
    user = user_service.get_user_by_clerk_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")
    return user
