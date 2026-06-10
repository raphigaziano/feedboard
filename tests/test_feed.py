import logging
from unittest.mock import patch

from feedparser.util import FeedParserDict

from feedboard.main import Config
from feedboard.feed import Feed, merge_feeds


FEED_DATA = [
    FeedParserDict({
        'feed': {
            'title': 'Test Feed 1',
        },
        'entries': [
            {
                'title': 'First article',
                'published_parsed': 3,
                'link': '/first-article',
            },
            {
                'title': 'Second article',
                'published_parsed': 1,
                'link': '/second-article',
            },
        ]
    }),
    FeedParserDict({
        'feed': {
            'title': 'Test Feed 2',
        },
        'entries': [
            {
                'title': 'Yet Another Article',
                'updated_parsed': 2,
                'link': '/yet-another-article',
            },
        ]
    }),
]


def test_basic_feed():
    """ Basic feed construction """

    feed1 = Feed(FEED_DATA[0])
    feed2 = Feed(FEED_DATA[1])

    assert feed1.title == 'Test Feed 1'
    assert feed2.title == 'Test Feed 2'

    entries1 = list(feed1.entries)
    assert len(entries1) == 2

    assert entries1[0].feed is feed1
    assert entries1[1].feed is feed1

    entries2 = list(feed2.entries)
    assert len(entries2) == 1

    assert entries2[0].feed is feed2


@patch('feedboard.feed.feedparser.parse', return_value=FEED_DATA[0])
def test_feed_from_url(parse_feed):
    url = "http://dummy.com/feed.xml"
    feed = Feed.from_url(url)
    parse_feed.assert_called_once_with(url)
    assert feed.title == 'Test Feed 1'


def test_feed_from_url_parse_error(caplog):
    caplog.set_level(logging.WARNING)
    url = "tests/data/feeds/noxml.xml"
    feed = Feed.from_url(url)
    assert feed.data.bozo
    assert len(feed.data.entries) == 0
    assert len(list(feed.entries)) == 0
    assert f"Could not parse feed for url {url}:" in caplog.text


@patch('feedboard.feed.feedparser.parse', return_value=FEED_DATA[1])
def test_feed_from_dict(parse_feed):
    url = "http://dummy.com/feed.xml"
    feed = Feed.from_dict({'url': url, 'meta': 'data'})
    parse_feed.assert_called_once_with(url)
    assert feed.title == 'Test Feed 2'
    assert feed.meta == {'meta': 'data'}


def test_entry_published_fallback():
    """ Explicit test on the fallback logic for the published field """
    feed = Feed(FEED_DATA[1])
    entry = list(feed.entries)[0]
    assert entry.published == 2


def test_merge_feeds():
    """ Merging several feeds """

    feed1 = Feed(FEED_DATA[0])
    feed2 = Feed(FEED_DATA[1])

    entries = merge_feeds([feed1, feed2], Config())
    assert [e.published for e in entries] == [3, 2, 1]
