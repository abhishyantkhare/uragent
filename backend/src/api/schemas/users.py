from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SignInMethod(str, Enum):
    CLERK = "CLERK"


class CreateUserRequest(BaseModel):
    email: str
    name: Optional[str] = None
    clerk_id: Optional[str] = None
    sign_in_method: Optional[str] = SignInMethod.CLERK
