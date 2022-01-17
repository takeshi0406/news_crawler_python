from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, validator
from news_crawler.valueobjects.url import Url
from news_crawler.lib.constants import YESTERDAY, JST


class TweetData(BaseModel):
    created_at: datetime
    id: int
    favorite_count: int
    retweet_count: int
    text: str
    expanded_urls: list[Url]

    @property
    def counts(self) -> int:
        return self.favorite_count + self.retweet_count

    def is_target(self) -> bool:
        return self.was_created_at_yesterday() and self.counts >= 1

    def was_created_at_yesterday(self) -> bool:
        return self.created_at.date() == YESTERDAY

    @classmethod
    def from_tweet(cls, data: dict) -> TweetData:
        return cls(
            **data,
            expanded_urls=[Url(url=x["expanded_url"]) for x in data["entities"]["urls"]]
        )

    @validator("created_at", pre=True)
    def parse_birthdate(cls, value: str) -> datetime:
        date = datetime.strptime(value, "%a %b %d %H:%M:%S %z %Y")
        return date.astimezone(JST)
