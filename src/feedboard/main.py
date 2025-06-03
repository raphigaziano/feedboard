from feedboard.feed import get_all_feeds
from feedboard.html import generate_html


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
    entries = get_all_feeds(FEED_URLS)
    output = generate_html(entries, 'template.html')
    if output:
        print(output)
