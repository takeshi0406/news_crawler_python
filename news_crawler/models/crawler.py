import re
import unicodedata
import trio
import httpx
from bs4 import BeautifulSoup
from news_crawler.valueobjects.summarized_url import SummarizedUrl, PageData
from news_crawler.valueobjects.url import Url
from news_crawler.valueobjects.tweet import TweetData


def fetch_pages(urls: list[SummarizedUrl]) -> list[PageData]:
    async def _inner():
        return await _fetch_pages(urls)

    return trio.run(_inner)


async def _fetch_pages(urls: list[SummarizedUrl], *, count: int = 0) -> list[PageData]:
    await trio.sleep(count)

    if len(urls) == 0 or count >= 3:
        return [PageData(redirected_url=Url(url=u), title=None) for u in urls]

    results = []
    failed_urls = []

    async def _inner(client, url: SummarizedUrl):
        try:
            response = await client.get(url.url.get_uniq_url(), follow_redirects=True)
            results.append(
                _parse_html(
                    redirected_url=Url(url=str(response.url)),
                    html=response.text,
                    sources=url.sources,
                )
            )
        except Exception as e:
            print(type(e), e)
            failed_urls.append(url)

    async with httpx.AsyncClient(timeout=20) as client:
        async with trio.open_nursery() as nursery:
            for url in urls:
                nursery.start_soon(_inner, client, url)

    return results + await _fetch_pages(failed_urls, count=count + 1)


def _parse_html(redirected_url: str, html: str, sources: list[TweetData]) -> PageData:
    soup = BeautifulSoup(html, "lxml")
    if soup.title is None or len(soup.title.text) == 0:
        title = None
    else:
        title = _regularize_title(soup.title.text)
    return PageData(redirected_url=redirected_url, title=title, sources=sources)


def _regularize_title(title: str) -> str:
    return unicodedata.normalize("NFKC", re.sub(r"\s+", " ", title)).strip()
