import feedparser

FEED_URLS = {
    'Tech': [
        'https://ploum.net/atom.xml',
        'https://lucumr.pocoo.org/feed.atom',
    ],
    'My crap': [
        'https://www.rgaz.fr/feeds/atom.xml',
    ],
}


class Entry:

    def __init__(self, feed_title, raw_data: dict):
        self.feed_title = feed_title
        self.raw_data = raw_data

    @property
    def title(self):
        return self.raw_data['title']

    @property
    def published(self):
        return self.raw_data.get('published', self.raw_data['updated'])


class Feed:

    def __init__(self, data):
        self.data = data

    @property
    def title(self):
        return self.data['feed']['title']

    @property
    def entries(self):
        for e in self.data.entries:
            yield Entry(self.title, e)

    @classmethod
    def from_url(cls, url):
        parsed_feed = feedparser.parse(url)
        return cls(parsed_feed)


def get_feed(feed_url):
    return Feed.from_url(feed_url)
