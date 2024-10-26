from typing import Annotated, List

from fastapi import APIRouter, Depends
from src.api.auth import auth_required
from src.api.schemas.seeds import ListSeedsResponse
from src.dependencies import SeedServiceClient
from src.services.seed_service.types import Seed
from src.services.user_service.types import User

router = APIRouter()


@router.get("/seeds", response_model=ListSeedsResponse)
async def get_seeds_by_user(
    user: Annotated[User, Depends(auth_required)], seed_service: SeedServiceClient
):
    seeds = seed_service.get_seeds_by_user_id(user.id)
    return ListSeedsResponse(seeds=seeds)
