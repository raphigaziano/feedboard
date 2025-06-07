import sys
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

    OUTPUT = sys.stdout

    # Those cannot have default values
    TEMPLATE_PATH = ''
    FEED_URLS = {}

    def __init__(self):
        pass

    def get_property_names(self):
        """ Return list of setting names """
        for k, v in self.__class__.__dict__.items():
            if not k.isupper():
                continue
            yield k

    def get_prop(self, propname, obj):
        return (
            getattr(obj, propname, None) or
            getattr(obj, propname.replace('_', '-').lower(), None))

    def update(self, updater):
        """ Update values provided by the updater object. """
        for propname in self.get_property_names():
            if (updated := self.get_prop(propname, updater)):
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
    config.update(args)
    return config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings')
    parser.add_argument('-o', '--output')
    return parser.parse_args()


def write_output(output, config):
    if not output:
        return
    try:
        config.OUTPUT.write(output)
    except AttributeError:
        with open(config.OUTPUT, 'w') as of:
            of.write(output)


def main():
    """ Main entry point. """
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)
    if not (config := get_config(args)):
        return

    entries = get_all_feeds(config)

    output = generate_html(entries, config.TEMPLATE_PATH)
    write_output(output, config)
