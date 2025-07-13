from feedboard.main import Config
from feedboard.feed import Entry, Feed, merge_feeds


FEED_DATA = [
    {
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
    },
    {
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
    },
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
