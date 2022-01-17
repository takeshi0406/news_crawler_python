from collections import defaultdict
from news_crawler.valueobjects.tweet import TweetData
from news_crawler.valueobjects.summarized_url import (
    SummarizedUrl,
    PageData,
    SummarizedPageData,
)


def summarize_tweets(tweets: list[TweetData]) -> list[SummarizedUrl]:
    results = defaultdict(list)
    for tweet in tweets:
        for url in tweet.expanded_urls:
            if url.is_target_url():
                results[url].append(tweet)
    return [SummarizedUrl(url=k, sources=v) for k, v in results.items()]


def summarize_pages(pages: list[PageData]) -> list[SummarizedPageData]:
    results = defaultdict(list)
    for page in pages:
        if page.redirected_url.is_target_url():
            results[page.redirected_url].append(page)
    return [
        SummarizedPageData(
            url=k, title=v[0].title, sources=sum([x.sources for x in v], [])
        )
        for k, v in results.items()
    ]
