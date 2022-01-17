from news_crawler.lib.slack import SlackClient
from news_crawler.valueobjects.summarized_url import SummarizedPageData
from news_crawler.lib.constants import YESTERDAY


class SlackNotifier:
    def __init__(self, title: str, endpoint: str):
        self.slack = SlackClient(endpoint=endpoint)
        self.title = title

    def post_message(self, pages: list[SummarizedPageData]):
        message = self._build_message(pages)
        # print(message)
        self.slack.send_message(message)

    def _build_message(self, pages: list[SummarizedPageData]) -> str:
        if len(pages) == 0:
            return "ニュースが存在しません"

        sorted_pages = list(sorted(pages, key=lambda p: p.counts, reverse=True))
        message = "\n\n".join(
            f":emo_star:×{x.counts}\n{x.get_title()}\n{x.url.get_uniq_url()}"
            for x in sorted_pages[:30]
        )
        return f':rolled_up_newspaper:*{YESTERDAY.strftime("%Y年%-m月%-d日")}の{self.title}ニュース*:rolled_up_newspaper:\n\n{message}'
