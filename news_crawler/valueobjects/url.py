from __future__ import annotations
import re
from pydantic import BaseModel
from urllib.parse import parse_qs, urlparse, parse_qsl, ParseResult

NONTARGET_NETLOCS = {"twitter.com", "gyazo.com"}
UNUSED_QUERIES = {
    "utm_source",
    "utm_content",
    "utm_campaign",
    "utm_medium",
    "utm_term",
    "cmpid",
    "feedType",
    "feedName",
    "n_cid",
    "cmpid=",
    "feature",
    "body",
    "from",
    "ref",
    "cid",
    "share",
    "fbclid",
    "pagefrom",
    "hss_channel",
    "rss",
    # AWS event
    "sc_channel",
    "sc_campaign",
    "sc_publisher",
    "sc_country",
    "sc_geo",
    "sc_outcome",
    "trk",
    "sc_content",
    "linkId",
}


class Url(BaseModel):
    url: str

    def __hash__(self) -> int:
        return hash(self.get_uniq_url())

    def __eq__(self, other: Url) -> bool:
        return self.get_uniq_url() == other.get_uniq_url()

    def is_target_url(self) -> bool:
        parsed = urlparse(self.url)
        return parsed.netloc != "twitter.com" and len(parsed.path) >= 2

    def get_uniq_url(self) -> str:
        parsed = urlparse(self.url)
        if parsed.netloc in {"www.amazon.co.jp", "amazon.co.jp"}:
            return _regularize_amazon_url(self.url)
        elif parsed.netloc == "b.hatena.ne.jp":
            return _regularize_hatena_bookmark_url(self.url)
        else:
            return _regularize_url(self.url)


def _regularize_amazon_url(url: str) -> str:
    for regex in [r"(https?:\/\/[^\/]*\/).*(dp\/[^\/|\?]*)"]:
        if matched := re.search(regex, url):
            return "".join(matched.groups())
    return _regularize_url(url)


def _regularize_hatena_bookmark_url(url: str) -> str:
    for protocol, regex in [("https", r"\/entry\/s\/(.+)"), ("http", r"\/entry\/(.+)")]:
        if matched := re.search(regex, url):
            return _regularize_url(f"{protocol}://{matched.groups()[0]}")
    return _regularize_url(url)


def _regularize_url(url: str) -> str:
    parsed = urlparse(url)
    return ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path,
        query="&".join(
            f"{k}={v}" for k, v in parse_qsl(parsed.query) if k not in UNUSED_QUERIES
        ),
        params=parsed.params,
        fragment="",
    ).geturl()
