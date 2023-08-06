
from pelican import signals
import os

from webassets import Environment
from webassets.ext.jinja2 import AssetsExtension

import logging
logger = logging.getLogger(__name__)


def add_extension(pelican):
    """add webassets' jinja2 extension to pelican"""
    jinja_env = pelican.settings['JINJA_ENVIRONMENT']
    if type(jinja_env) == dict:  # pelican 3.7+
        jinja_env = jinja_env['extensions']
    jinja_env.append(AssetsExtension)
    logger.debug("'pelican-webassets' added to jinja2 environment")


def create_environment(generator):
    """define the webassets environment for the generator"""

    theme_static_dir = generator.settings['THEME_STATIC_DIR']
    assets_destination = os.path.join(generator.output_path, theme_static_dir)
    generator.env.assets_environment = Environment(
        assets_destination, theme_static_dir)

    # are we in debug mode?
    in_debug = generator.settings.get(
        'WEBASSETS_DEBUG', logger.getEffectiveLevel() <= logging.DEBUG
    )
    if in_debug:
        logger.info("'webassets' running in DEBUG mode")
    generator.env.assets_environment.debug = in_debug

    # pass along the additional congiuration options
    for item in generator.settings.get('WEBASSETS_CONFIG', []):
        generator.env.assets_environment.config[item[0]] = item[1]
        logger.debug(
            "'webassets' adding config: '%s' -> %s",
            item[0], item[1]
        )

    # pass along the named bundles
    for name, args, kwargs in generator.settings.get('WEBASSETS_BUNDLES', []):
        generator.env.assets_environment.register(name, *args, **kwargs)
        logger.debug("'webassets' registered bundle: '%s'", name)

    # pass along the additional directories for webassets
    paths = (
        generator.settings['THEME_STATIC_PATHS'] +
        generator.settings.get('WEBASSETS_SOURCE_PATHS', [])
    )
    logger.debug("'webassets' looding for files in: %s", paths)
    for path in (paths):
        generator.env.assets_environment.append_path(
            os.path.join(generator.theme, path)
        )


def register():
    signals.initialized.connect(add_extension)
    signals.generator_init.connect(create_environment)
