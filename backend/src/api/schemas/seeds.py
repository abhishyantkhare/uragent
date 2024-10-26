from pydantic import BaseModel
from src.services.seed_service.types import Seed


class ListSeedsResponse(BaseModel):
    seeds: list[Seed]
