import os
import yaml


def resolve_parent(dir, configs=None):
    '''Resolve the parent config from start directory.

    It will return a list of config, from parent to child.

    Each object is added a `path` key that contains its path.

    The `configs` variable is an accumulator. You can put a dict in
    it so the function will check whether to search for parent configs
    according to the `extend` value.
    '''

    dir = os.path.abspath(dir)

    if not configs:
        configs = []
    elif len(configs) == 0:
        pass
    elif 'extend' in configs[0] and not configs[0]['extend']:
        return configs

    try:
        path = dir + '/.mdrc'
        parent = yaml.load(open(path, 'r'))
        parent['_dir'] = os.path.dirname(path)
        configs.insert(0, parent)
    except FileNotFoundError:
        pass

    # Stop at root
    if dir == '/':
        return configs

    # Go parent recursively
    return resolve_parent(os.path.dirname(dir), configs)


def resolve(config_file, input_file):
    '''Resolve the config from context.

    If there is a `config_file`, read it and all the eventual parent
    `.mdrc` while `extend` is `True` to create the config object.

    Otherwise, try to find any parent `.mdrc` of `input_file` with the
    same rules.

    If there is no `input_file` either, the CWD is used to search for
    config (see `resolve_parent`).
    '''

    if not config_file:
        dir = os.path.dirname(input_file) if input_file else os.getcwd()
        return resolve_parent(dir)

    config = yaml.load(open(config_file, 'r'))
    return resolve_parent(os.path.dirname(config_file), [config])


def merge(configs, parse=None):
    '''Merge a config list.

    `parse` is a callback to modify a config object on the fly.
    '''

    if not len(configs):
        return {}

    if not parse:
        parse = lambda x: x

    # Convert each dict items to list for the `+` operator
    config = list(parse(configs.pop(0)).items())

    for i in configs:
        # Add the next dict as a list
        config += list(parse(i).items())

    # Build everything back to a dict
    return dict(config)


def parse(config):
    '''Parse a config object.

    Some known config keys like `layout` are resolved according to the
    config `path` value.
    '''

    if 'layout' in config:
        if config['layout'] == 'default':
            config['layout'] = None
        else:
            config['layout'] = config['_dir'] + '/' + config['layout']

    return config


def find(config_file, input_file, meta):
    '''Find the config for given context.

    If `meta.extend` is `False`, nothing will be added.

    Otherwise, the parent config files are resolved with
    `resolve` according to `config_file` and `input_file` (see `resolve`
    documentation).
    '''

    # The config tree
    configs = []

    # Find parent config if allowed
    if 'extend' not in meta or meta['extend']:
        configs = resolve(config_file, input_file)

    # Add the meta at the end (most important)
    configs.append(meta)

    # Merge everything
    return merge(configs, parse)
