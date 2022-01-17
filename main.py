import functions_framework
from news_crawler.lib.config import read_config
from news_crawler.lib.twitter import TwitterClient
from news_crawler.models import crawler, url_summarizer, notifier


@functions_framework.cloud_event
def hello_cloud_event(cloud_event):
    print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")


def main():
    for config in read_config("./config.yml").confs:
        proc = MainClass(title=config.title, endpoint=config.endpoint)
        proc.run(config.twitter)


class MainClass:
    def __init__(self, title: str, endpoint: str):
        self.twitter = TwitterClient()
        self.slack = notifier.SlackNotifier(title=title, endpoint=endpoint)

    def run(self, twitter_list_name: str):
        tweets = self.twitter.get_list_timeline(twitter_list_name)
        filtered_tweets = filter(lambda t: t.is_target(), tweets)
        urls = url_summarizer.summarize_tweets(filtered_tweets)
        pages = crawler.fetch_pages(urls)
        results = url_summarizer.summarize_pages(pages)
        self.slack.post_message(results)


if __name__ == "__main__":
    main()
