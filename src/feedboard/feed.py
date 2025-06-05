import logging
import itertools
from concurrent.futures import ThreadPoolExecutor

import feedparser

logger = logging.getLogger(__file__)


class Entry:
    """
    A fully parsed RSS / Atom feed.

    This is a simple wrapper around a FeedParserDict, with shortcuts to the
    most commonly accessed fields.

    """

    def __init__(self, feed, raw_data: dict):
        self.feed = feed
        self.raw_data = raw_data

    @property
    def title(self):
        return self.raw_data['title']

    @property
    def link(self):
        return self.raw_data['link']

    @property
    def published(self):
        """
        Will fallback on the `updated` field if `published` is not present.
        Return None if nothing can be found.
        """
        return self.raw_data.get(
            'published_parsed', self.raw_data.get('updated_parsed'))


class Feed:
    """
    An individual Feed Entry.

    This is a simple wrapper around a FeedParserDict, with shortcuts to the
    most commonly accessed fields.

    """

    def __init__(self, data):
        self.data = data

    @property
    def title(self):
        return self.data['feed']['title']

    @property
    def entries(self):
        for e in self.data['entries']:
            yield Entry(self, e)

    @classmethod
    def from_url(cls, url):
        logger.debug(f"Downloading feed ({url})...")
        parsed_feed = feedparser.parse(url)
        logger.debug(f"Done ({url})")
        return cls(parsed_feed)


def merge_feeds(feed_list, config):
    """
    Return a regular list of entries from all the passed feeds, sorted by
    descending date of publication.

    """
    yield from sorted(
        itertools.chain.from_iterable(
            itertools.islice(f.entries, config.max_entries)
            for f in feed_list),
        key=lambda e: e.published,
        reverse=True
    )


def download_feed_list(feed_urls, config):
    feeds = []
    n_workers = max(1, config.max_workers // 3 * 2)
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        executor.map(lambda url: feeds.append(Feed.from_url(url)), feed_urls)
    return feeds


def get_all_feeds(config):
    """
    Retrieve all feeds from the passed config dict and aggregate all their
    entries, keeping them mapped to their respective categories.

    """
    r = {}
    n_workers = max(1, config.max_workers // 3)
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        def process_category(t):
            cat, feed_urls = t
            feeds = download_feed_list(feed_urls, config)
            r[cat] = merge_feeds(feeds, config)
        executor.map(process_category, config.FEED_URLS.items())
    return r
