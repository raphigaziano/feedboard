import os
import time
import logging
import jinja2


logger = logging.getLogger(__file__)


def load_template(filepath):
    """
    Custom loader function for jinja2.

    Just treat the template name as its file path so that we can open any
    arbitrary file.
    """
    if not os.path.isfile(filepath):
        logger.error("Could not find template: %s", filepath)
        return ''

    with open(filepath, 'r') as f:
        return f.read()


def _jinja2_filter_timefmt(t, fmt=None):
    """ Quick & dirty time formatting filter. """
    if fmt:
        return time.strftime(fmt, t)
    else:
        return time.strftime('%m/%d/%Y', t)


def get_jinja_env():
    """ Jinja2 initialization. """
    env = jinja2.Environment(
        loader=jinja2.FunctionLoader(load_template),
        autoescape=True,
        trim_blocks=True,
    )
    env.filters['time_fmt'] = _jinja2_filter_timefmt
    return env


def generate_html(entries, env, template_path):
    """ Generate an html view of the passed feed entries. """
    t = env.loader.load(env, template_path)
    return t.render(entries=entries)
