from enum import Enum


class TwitterSeedSourceType(str, Enum):
    BOOKMARKS = "bookmarks"
    FEED = "feed"
