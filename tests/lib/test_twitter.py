from news_crawler.lib import twitter


def test_twotter():
    client = twitter.TwitterClient()
    tweets = client.get_list_timeline("takeshi0406/dev")
    assert len(tweets) > 100
