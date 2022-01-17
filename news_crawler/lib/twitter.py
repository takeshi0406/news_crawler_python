import twitter
from news_crawler.lib.settings import settings
from news_crawler.valueobjects.tweet import TweetData


class TwitterClient:
    def __init__(self):
        self.api = twitter.Api(
            consumer_key=settings.twitter_consumer_key,
            consumer_secret=settings.twitter_consumer_secret,
            access_token_key=settings.twitter_token,
            access_token_secret=settings.twitter_token_secret,
        )

    def get_list_timeline(self, twlist: str) -> list[TweetData]:
        owner_screen_name, slug = twlist.split("/")
        return [
            TweetData.from_tweet(t)
            for t in self.api.GetListTimeline(
                slug=slug,
                owner_screen_name=owner_screen_name,
                include_rts=True,
                count=200,
                return_json=True,
            )
        ]
