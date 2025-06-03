import os
import logging
import argparse
import importlib

from feedboard.feed import get_all_feeds
from feedboard.html import generate_html

logger = logging.getLogger()

DEFAULT_CONFIG_PATH = './feedboardconf.py'


def get_config(config_path):
    """ Load configuration module from an arbitrary path. """
    loader = importlib.machinery.SourceFileLoader(
        'config',
        os.path.abspath(config_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    try:
        loader.exec_module(mod)
    except FileNotFoundError:
        logger.error("Could not load configuration file: %s", config_path)
        return None

    return mod


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings')
    return parser.parse_args()


def main():
    """ Main entry point. """
    args = parse_args()
    if not (config := get_config(args.settings or DEFAULT_CONFIG_PATH)):
        return

    entries = get_all_feeds(config.FEED_URLS)
    output = generate_html(entries, config.TEMPLATE_PATH)
    if output:
        print(output)
