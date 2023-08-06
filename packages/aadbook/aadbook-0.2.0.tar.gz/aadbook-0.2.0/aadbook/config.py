#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import configparser
import logging
import os

from .auth import Auth
from .storage import Storage
from os.path import realpath, expanduser

log = logging.getLogger(__name__)

TEMPLATE = '''\
# "#" or ";" at the start of a line makes it a comment.
[DEFAULT]
# The following are optional, defaults are shown

# This file is written by the Azure AD library, and should be kept secure,
# it's like a password to your AD contacts.
;auth_db_filename: ~/.aadbook_auth.json

;cache_filename: ~/.aadbook_cache
;cache_expiry_hours: 24
'''


def read_config(config_file):
    '''Reads the ~/.aadbookrc and any authentication data
    returns the configuration as a dictionary.

    '''
    config = Storage({  # Default values
        'cache_filename': '~/.aadbook_cache',
        'auth_db_filename': '~/.aadbook_auth.json',
        'cache_expiry_hours': '24'})
    config_file = os.path.expanduser(config_file)
    parser = _get_config(config_file)
    if parser:
        config.get_dict().update(dict(parser.items('DEFAULT', raw=True)))

    # Ensure paths are fully expanded
    config.cache_filename = realpath(expanduser(config.cache_filename))
    config.auth_db_filename = realpath(expanduser(config.auth_db_filename))

    config.auth = Auth(config.auth_db_filename)
    # config.creds = config.store.get()

    log.debug(config)
    return config


def _get_config(config_file):
    '''find, read and parse configuraton.'''
    parser = configparser.SafeConfigParser()
    if os.path.lexists(config_file):
        try:
            log.info('Reading config: %s', config_file)
            inp = open(config_file)
            parser.readfp(inp)
            return parser
        except (IOError, configparser.ParsingError) as err:
            raise ConfigError("Failed to read configuration %s\n%s" % (config_file, err))
    return None


class ConfigError(Exception):
    pass
