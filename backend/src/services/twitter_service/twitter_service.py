import os
import uuid

import tweepy
from src.services.seed_service.seed_service import SeedService
from src.services.seed_service.types import OAuthInfo, Seed, SeedType
from src.services.twitter_service.constants import TWITTER_REFRESH_TOKEN_ENDPOINT


class TwitterService:
    def __init__(self, seed_service: SeedService):
        self.seed_service = seed_service
        self.auth_client = tweepy.OAuth2UserHandler(
            client_id=os.environ.get("TWITTER_CLIENT_ID"),
            client_secret=os.environ.get("TWITTER_CLIENT_SECRET"),
            redirect_uri="http://localhost:3000/twitter-auth-success",
            scope=["tweet.read", "users.read", "bookmark.read", "offline.access"],
        )

    def get_auth_url(self):
        return self.auth_client.get_authorization_url()

    def set_access_token(self, user_id: uuid.UUID, auth_response_url: str):
        # Check if the seed already exists
        existing_seed = self.seed_service.get_seed_by_user_id_and_seed_type(
            user_id=user_id, seed_type=SeedType.TWITTER
        )
        if existing_seed:
            return
        try:
            token_dict = self.auth_client.fetch_token(auth_response_url)
            self.seed_service.create_seed(
                user_id=user_id,
                auth_info=OAuthInfo(**token_dict),
                seed_type=SeedType.TWITTER,
            )
        except Exception as e:
            print(e)
            raise e

    def is_twitter_authenticated(self, user_id: uuid.UUID):
        existing_seed = self.seed_service.get_seed_by_user_id_and_seed_type(
            user_id=user_id, seed_type=SeedType.TWITTER
        )
        return existing_seed is not None

    def get_user_bookmarks(self, twitter_seed: Seed):
        token = self.get_twitter_auth_token_from_seed_or_refresh(twitter_seed)
        client = tweepy.Client(
            bearer_token=token,
        )
        bookmarks = client.get_bookmarks(expansions=["author_id"])
        return bookmarks

    def get_user_feed(self, twitter_seed: Seed):
        token = self.get_twitter_auth_token_from_seed_or_refresh(twitter_seed)
        client = tweepy.Client(bearer_token=token)
        feed = client.get_home_timeline(expansions=["author_id"])
        return feed

    def get_twitter_auth_token_from_seed_or_refresh(self, twitter_seed: Seed):
        token = twitter_seed.auth_info.access_token
        if twitter_seed.auth_info.is_token_expired():
            token = self.auth_client.refresh_token(
                TWITTER_REFRESH_TOKEN_ENDPOINT, twitter_seed.auth_info.refresh_token
            )
            self.seed_service.update_seed_auth_info(twitter_seed.id, OAuthInfo(**token))
        return token
