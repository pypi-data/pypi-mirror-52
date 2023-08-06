# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class ConfigError(Exception):
    pass


class ConfigKeyError(ConfigError, KeyError):
    def __init__(self, key):
        super(ConfigKeyError, self).__init__(
            "Config value '{}' does not exist".format(key)
        )
