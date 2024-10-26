import uuid
from typing import List

from src.dependencies import (
    agent_service_dependency,
    seed_service_dependency,
    twitter_service_dependency,
)
from src.services.agent_service.types import AgentSeed
from src.services.seed_service.types import Seed, SeedType
from src.services.twitter_service.types import TwitterSeedSourceType
from src.workflows.agent_seeding.types import (
    GetAgentSeedsParams,
    ProcessTwitterSeedParams,
)
from temporalio import activity


@activity.defn
def get_agent_seeds(params: GetAgentSeedsParams) -> List[AgentSeed]:
    agent_service = agent_service_dependency.get()
    return agent_service.get_agent_seeds(params.user_id, params.agent_id)


@activity.defn
def get_seed_for_agent(agent_seed: AgentSeed) -> Seed:
    # Fetch the seed
    seed_service = seed_service_dependency.get()
    seed = seed_service.get_seed_by_id(agent_seed.user_id, agent_seed.seed_id)
    return seed


@activity.defn
def process_twitter_seed(params: ProcessTwitterSeedParams):
    twitter_service = twitter_service_dependency.get()
    tweets = []
    for source in params.agent_seed.actions.sources:
        if source.type == TwitterSeedSourceType.BOOKMARKS:
            bookmarks = twitter_service.get_user_bookmarks(params.twitter_seed)
            tweets.extend(bookmarks["data"])
        if source.type == TwitterSeedSourceType.FEED:
            feed = twitter_service.get_user_feed(params.twitter_seed)
            tweets.extend(feed["data"])
    tweet_docs = []
    for tweet in tweets:
        tweet_docs.append(
            {
                "text": tweet["text"],
                "source_item_id": tweet["id"],
                "source_type": SeedType.TWITTER,
                "item_url": f"https://twitter.com/{tweet['author_id']}/status/{tweet['id']}",
            }
        )
    return tweet_docs


@activity.defn
def embed_docs_for_agent(docs: List[dict]):
    pass
