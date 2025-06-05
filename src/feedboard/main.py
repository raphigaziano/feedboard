import os
import logging
import argparse
import importlib

from feedboard.feed import get_all_feeds
from feedboard.html import generate_html

logger = logging.getLogger(__file__)

DEFAULT_CONFIG_PATH = './feedboardconf.py'


class Config:
    """
    Namespace for configuration.
    Provides default values and a way to update those based on passed in
    objects.

    """
    MAX_WORKERS = 12
    MAX_ENTRIES = 20    # per category

    # Those cannot have default values
    TEMPLATE_PATH = ''
    FEED_URLS = []

    def __init__(self):
        pass

    def get_property_names(self):
        """ Return list of setting names """
        for k, v in self.__class__.__dict__.items():
            if not k.isupper():
                continue
            yield k

    def update(self, updater):
        """ Update values provided by the updater object. """
        for propname in self.get_property_names():
            if (updated := getattr(updater, propname, None)):
                setattr(self, propname, updated)

    def print(self):
        """ Debug printing. """
        for propname in self.get_property_names():
            print(f'{propname}: {getattr(self, propname)}')


def load_config(config_path):
    """ Load configuration module from an arbitraty path. """
    loader = importlib.machinery.SourceFileLoader(
        'config',
        os.path.abspath(config_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    try:
        loader.exec_module(mod)
    except FileNotFoundError:
        logger.error(f"Could not load configuration file: {config_path}")
        return None
    return mod


def get_config(args):
    """ Load configuration module from an arbitrary path. """
    mod = load_config(args.settings or DEFAULT_CONFIG_PATH)
    if not mod:
        return None
    config = Config()
    config.update(mod)
    # TODO: override from args
    return config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings')
    return parser.parse_args()


def main():
    """ Main entry point. """
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)
    if not (config := get_config(args)):
        return

    entries = get_all_feeds(config)

    output = generate_html(entries, config.TEMPLATE_PATH)
    if output:
        print(output)
