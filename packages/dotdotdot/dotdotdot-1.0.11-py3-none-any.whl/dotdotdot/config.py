# -*- coding: utf-8 -*-
"""
config: Load application configuration and return an object representation.

Allows accessing configuration using "dot-notation" for supported configuration
file formats.

Supported formats are:
  * yml
  * TODO: ini
  * TODO: json
"""

import yaml

# from enum import Enum


# Formats = Enum('Formats', names=[('yml', 1), ('ini', 2)])


def repr_fx(self):
    """
    Object representation. Function gets added as a method
    to generated classes.

    :return: string object representation
    """
    return yaml.dump(self)


def str_fx(self):
    """
    String representation. Function gets added as a method
    to generated classes.

    :return: string object representation
    """
    return yaml.dump(self, default_flow_style=False)


def get_fx(self, key, default=None):
    """
    Allow for c.get(foo) invocation.

    :param self: Config object
    :param key: config key to look for
    :param default: value if key is missing
    :return:
    """
    key_exists = hasattr(self, key)
    if key_exists:
        return get_item_fx(self, key)
    elif default:
        return default
    else:
        raise KeyError


def get_item_fx(self, key):
    """
    Function to implement __getitem__

    :param self:
    :param key:
    :return:
    """
    if hasattr(self, key):
        return getattr(self, key)
    else:
        raise KeyError


def __validate():
    """
    Hook to validate config.

    :return:
    """
    # TODO: implement


def __determine_config_type():
    """
    Find out the type of the configuration file.
    :return:
    """


class Config(object):
    """
    The configuration object that will be populated.
    """
    pass


Config.__repr__ = repr_fx
Config.__str__ = str_fx
Config.__getitem__ = get_item_fx
Config.get = get_fx


def __construct(config, yml):
    """
    Recursive function to construct an object corresponding to given value.

    Adds elements from the input yaml to the configuration object in the first
    argument. For complex value types recursively instantiates new objects and
    attaches them into the configuration tree.

    The intent is to be able to access the yaml config using dot notation -
    e.g. config.a.b.c.

    :param config: The config object to populate.
    :param yml: The yaml corresponding to the conf parameter.
    """

    for key in yml:
        if type(yml[key]) == dict:
            # create an object for the subsection
            klass = type(key, (), {})
            klass.__repr__ = repr_fx
            klass.__str__ = str_fx
            klass.__getitem__ = get_item_fx
            klass.get = get_fx
            obj = klass()
            __construct(obj, yml[key])
            setattr(config, key, obj)
        else:
            # just set simple value
            setattr(config, key, yml[key])


def load(paths):
    """
    Entry point for the config module.

    Load yml config files at specified path and convert to a config object.
    Merges the yaml files specified by the paths parameter - keys in a file
    later in the list override earlier keys.

    :param paths: List of complete paths of config files.
    :return Config object with member properties
    """
    if not paths:
        raise ConfigException(message='No configuration file specified',
                              reason=paths)
    yaml_dict = {}
    if type(paths) == str:
        paths = [paths]
    # for every filename in list...
    for path in paths:
        # read config file...
        with open(path) as f:
            # get config as dict...
            y = yaml.safe_load(f)
            # and merge into a single yaml dict.
            yaml_dict.update(y)
    config = Config()
    # get object for each key and set on the config object
    __construct(config, yaml_dict)

    return config


class ConfigException(Exception):
    def __init__(self, message, reason):
        self.message = message
        self.reason = reason

    def __str__(self):
        return repr(self.message)
