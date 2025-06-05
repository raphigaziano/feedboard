import os
import logging
import argparse
import importlib

from feedboard.feed import get_all_feeds
from feedboard.html import generate_html

logger = logging.getLogger(__file__)

DEFAULT_CONFIG_PATH = './feedboardconf.py'
DEFAULT_MAX_WORKERS = 12
DEFAULT_MAX_ENTRIES = 20    # per feed


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
    # TODO: merge with defaults
    mod.max_workers = getattr(mod, 'max_workers', DEFAULT_MAX_WORKERS) # what if it is zero ?
    mod.max_entries = getattr(mod, 'max_entries', DEFAULT_MAX_ENTRIES)
    return mod


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings')
    return parser.parse_args()


def main():
    """ Main entry point. """
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)
    if not (config := get_config(args.settings or DEFAULT_CONFIG_PATH)):
        return

    entries = get_all_feeds(config)

    output = generate_html(entries, config.TEMPLATE_PATH)
    if output:
        print(output)
