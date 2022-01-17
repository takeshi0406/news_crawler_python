from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from news_crawler.valueobjects.tweet import TweetData
from news_crawler.valueobjects.url import Url


class SummarizedUrl(BaseModel):
    url: Url
    sources: list[TweetData]


class PageData(BaseModel):
    redirected_url: Url
    title: Optional[str]
    sources: list[TweetData]


class SummarizedPageData(BaseModel):
    url: Url
    title: Optional[str]
    sources: list[TweetData]

    @property
    def counts(self) -> int:
        return sum(s.retweet_count + s.favorite_count for s in self.sources)

    def get_title(self) -> str:
        if self.title is None:
            return "[タイトルを取得できませんでした]"
        return self.title
