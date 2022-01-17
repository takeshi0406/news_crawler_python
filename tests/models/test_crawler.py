import trio
from news_crawler.models import crawler
from news_crawler.valueobjects.summarized_url import SummarizedUrl


def test_fetch():
    async def main():
        return await crawler._fetch_pages(
            [
                SummarizedUrl(
                    url="https://kiito.hatenablog.com/entry/2018/12/26/110317",
                    sources=[],
                ),
                SummarizedUrl(
                    url="https://t.co/RXvqzDEVAi",
                    sources=[],
                ),
                SummarizedUrl(
                    url="http://gihyo.jp",
                    sources=[],
                ),
            ]
        )

    results = trio.run(main)
    breakpoint()
    print(results)
    assert not results
