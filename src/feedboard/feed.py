import itertools

import feedparser


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
        parsed_feed = feedparser.parse(url)
        return cls(parsed_feed)


def merge_feeds(*feeds):
    """
    Return a regular list of entries from all the passed feeds, sorted by
    descending date of publication.

    """
    yield from sorted(
        itertools.chain.from_iterable(f.entries for f in feeds),
        key=lambda e: e.published,
        reverse=True
    )


def get_all_feeds(feed_config):
    """
    Retrieve all feeds from the passed config dict and aggregate all their
    entries, keeping them mapped to their respective categories.

    """
    r = {}
    for category, feed_urls in feed_config.items():
        r[category] = merge_feeds(*[Feed.from_url(url) for url in feed_urls])
    return r
