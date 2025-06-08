FEEDBOARD
=========

A simple tool to generate an aggregated rss feed. This is quick and dirty
and mostly intended for my own personal usage.

Usage:
------

- Install from github:
  ```bash
  $ pip install git+https://github.com/raphigaziano/feedboard
  ```

- Create a config file:

  ```python
    #feedboardconf.py

    # Template used to generate the html listing the aggregatted feeds
    TEMPLATE_PATH = './my_template.html'

    # Feeds must be split into categories, because that's how I want it for now.
    # Nothing's stopping you from definineg a single dummy category if you don't
    # need it.
    FEED_URLS = {
        'Cats': [
            'https://kitty.com/feed/atom.xml',
            '/path/to/local/feed.xml',          # urls can point to local files
        ],
        'Dogs': [
            'https://woof.net/rss.xml',
        ],
    }

    # Optional settings (default values)

    # How many threads to use.
    # One third of those will share categories, the other 2 thirds will handle
    # downloading individual feeds.
    MAX_WORKERS = 12

    # How many entries to keep, per category.
    MAX_ENTRIES = 20

    # File to write the generated html.
    OUTPUT = sys.stdout
  ```

- Write your template (save it as `TEMPLATE_PATH`):

  ```html
  {% for cat, cat_entries in entries|items %}
      <h2>{{ cat }}</h2>
      <ul>
      {% for e in cat_entries %}
          <li>
              {{ e.published|time_fmt }} - {{ e.feed.title }}
              <a href="{{ e.link }}" target="_blank">{{ e.title }} </a>
          </li>
      {% endfor %}
      </ul>
  {% endfor %}
  ```
  Templates are handled by [Jinja2](https://jinja.palletsprojects.com/en/stable/).
  A custom filter is provided for formatting dates (time_fmt).

- Run feedboard:

  ```bash
    $ # will look for configuration in $CWD/feedboardconf.py
    $ feedboard > output.html
    $ # specify a custom configuration file:
    $ feedboard --config=/path/to/my/config.py > output.html
  ```

  Individual settings can be overriden by turning them lower case and replacing
  underscores with dashes:

  ```bash
    $ feedboard --max-entries=100 --template-path=/path/to/template > output.html
  ```

I use a simple cronjob to update the generated page periodically.

Improvements:
------------

- Download feeds asynchronously.
- Allow overriding settings via command line arguments.
- profit.
