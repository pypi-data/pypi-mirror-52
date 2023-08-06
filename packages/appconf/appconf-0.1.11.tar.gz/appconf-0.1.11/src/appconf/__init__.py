# -*- coding: utf-8 -*-
__version__ = '0.1.11'

# stdlib imports
import os
import json
from os.path import abspath, exists, isabs, join, normpath

# 3rd party imports
import yaml

# local imports
from . import exc


class ConfigBase(object):
    config_file = 'appconf.yaml'
    version_var = 'version'
    env_prefix = 'APPCONF'
    version = '0'
    root_dir = abspath('.')
    defaults = {}
    deserializers = {}
    resolution = None

    def __init__(self, conf_path=None):
        self.conf_path = conf_path or self._discover_config()

    def load(self, conf_path=None, update=False):
        if conf_path is not None:
            self.conf_path = conf_path

        values = self._read()

        self._validate(values)
        self._deserialize(values)
        self._apply_defaults(values)
        self._apply_env(os.environ)

        if not update:
            self.values = values
        else:
            self.values.update(values)

        return self

    def get(self, name, *default):
        """ Get config value with the given name and optional default.

        :param str|unicode name:
            The name of the config value.
        :param Any default:
            If given and the key doesn't not exist, this will be returned instead.
            If it's not given and the config value does not exist, AttributeError
            will be raised
        :return Any:
            The requested config value. This is one of the global values defined
            in this file.
        """
        curr = self.values
        for part in name.split('.'):
            if part in curr:
                curr = curr[part]
            elif default:
                return default[0]
            else:
                raise exc.ConfigKeyError(name)

        return curr

    def path(self, path=None):
        """ Return absolute path to the repo dir (root project directory). """
        path = path or '.'

        if not isabs(path):
            path = normpath(join(self.root_dir, path))

        return path

    def get_path(self, name, *default):
        """ Get config value as path relative to the project directory.

        This allows easily defining the project configuration within the fabfile
        as always relative to that fabfile.

        :param str|unicode name:
            The name of the config value containing the path.
        :param Any default:
            If given and the key doesn't not exist, this will be returned instead.
            If it's not given and the config value does not exist, AttributeError
            will be raised
        :return Any:
            The requested config value. This is one of the global values defined
            in this file.
        """
        value = self.get(name, *default)

        if value is None:
            return None

        return self.path(value)

    def apply_to_dict(self, dct, mappings=None, mapfn=None):
        mappings = mappings or {}
        conf_table = []
        if mapfn is None:
            mapfn = lambda name: name

        for name, value in self.value_list():
            conf_name = mappings.get(name, mapfn(name))
            conf_table.append((name, conf_name, value))
            dct[conf_name] = value

    def value_list(self):
        return _list_dict_values(self.values)

    def _discover_config(self):
        """ Find configuration file.

        The config resolution is as follows:
        - dashboard.yaml
        - /etc/dashboard.yaml
        - <dashboard package>/run/config.yaml
        """
        resolution = self.resolution or [
            self.config_file,
            join('/etc', self.config_file),
        ]

        conf_path = next((x for x in resolution if exists(x)), None)
        if conf_path is None:
            raise RuntimeError('\n'.join([
                "No configuration found. Please provide one of:",
                "\n".join(resolution[:-1]),
                "Working Dir: {}".format(os.getcwd()),
            ]))

        return conf_path

    def _read(self):
        try:
            with open(self.conf_path) as fp:
                values = yaml.load(fp.read())

        except yaml.YAMLError as ex:
            raise exc.ConfigError("Failed to load config {}: {}".format(
                self.conf_path, str(ex)
            ))

        return values

    def _validate(self, values):
        if self.version_var not in values:
            raise RuntimeError("Unknown config version: {}".format(
                self.conf_path
            ))

        if values[self.version_var] != self.version:
            msg = "Unsupported config version: {}. Should be {}".format(
                json.dumps(values[self.version_var]), json.dumps(self.version)
            )
            raise RuntimeError(msg)

    def _deserialize(self, values):
        """ Deserialize raw config types into more complex python types.

        This is left as an extension point for app configs derived from this
        class.
        """
        for name, deserialize in self.deserializers.items():
            if name in values:
                values[name] = deserialize(values[name])

    def _apply_defaults(self, values):
        defaults = getattr(self, 'defaults', {})

        for name, value in defaults.items():
            values.setdefault(name, value)

    def _apply_env(self, env):
        prefix = self.env_prefix.upper() + '_'
        values = {k: v for k, v in env.items() if k.startswith(prefix)}
        for name, value in values:
            name = name[:len(prefix)]
            conf_name = name.lower().replace('__', '.')
            self.__set(conf_name, value)

    def __set(self, name, value):
        """ Set config variable with the given name to the given value.

        :param str|unicode name:
            The name of the config variable.
        :param Any value:
            The value to set.
        """
        curr = self.values
        parts = name.split('.')

        for part in parts[:-1]:
            curr = curr.setdefault(part, {})

        curr[parts[-1]] = value

def _list_dict_values(dct, prefix=''):
    result = []
    for name, value in sorted(dct.items(), key=lambda x: x[0]):
        full_name = '{}.{}'.format(prefix, name).strip('.')

        try:
            result += _list_dict_values(value, full_name)
        except AttributeError:
            result.append((full_name, value))

    return result
