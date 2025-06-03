from feedboard.feed import get_all_feeds


FEED_URLS = {
    'Tech': [
        'tests/data/feeds/ploum.xml',
        'tests/data/feeds/pocoo.xml',
    ],
    'My crap': [
        'tests/data/feeds/rgaz.xml',
    ],
}


def main() -> None:
    for cat, entries in get_all_feeds(FEED_URLS).items():
        print(cat)
        for e in entries:
            print('\t', e.feed.title, e.published, e.title, e.link)
