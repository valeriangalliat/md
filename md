#!/usr/bin/env python3

'''Usage: md [options] [<input>]

Arguments:
  <input>  Input file (`stdin` if not set).

Options:
  -h, --help       Show this screen.
  --version        Show version.
  --config=<file>  Try to find a `.mdconfig` (recursing in parent
                   directories) if not set.
  --layout=<file>  Layout file (will override configuration).
'''

import os
import pystache
import sys
import yaml

from docopt import docopt
from html.parser import HTMLParser
from io import StringIO
from markdown import markdown


DEFAULT_LAYOUT = '''<!DOCTYPE html>
<html{{#lang}} lang="{{lang}}"{{/lang}}>
<head>
<meta charset="utf-8">
<title>{{title}}</title>
</head>
<body>
{{{content}}}
</body>
</html>
'''


def file_or_def(arg, default):
    if arg:
        return open(arg, 'r')

    return default


def file_or_def_io(arg, default):
    return file_or_def(arg, StringIO(default))


def resolve_parent_config(dir, config_list=None):
    '''Resolve parent configuration from start directory.

    It will return a list of config objects, from parent to child.

    Each config object is added a `path` key that contains the
    config path.

    The `config_list` is an accumulator. You can put a config in it
    so the function will check whether to search for parent
    configurations according to the `extend` value.
    '''

    dir = os.path.abspath(dir)

    if not config_list:
        config_list = []
    elif 'extend' in config_list[0] and not config_list[0]['extend']:
        return config_list

    try:
        path = dir + '/.mdconfig'
        parent = yaml.load(open(path, 'r'))
        parent['_dir'] = os.path.dirname(path)
        config_list.insert(0, parent)
    except FileNotFoundError:
        pass

    if dir == '/':
        return config_list

    return resolve_parent_config(os.path.dirname(dir), config_list)


def resolve_config(config_file, markdown_file):
    '''Resolve configuration from context.

    If there is a `config_file`, read it and all the eventual parent
    `.mdconfig` while `extend` is `True` to create the config object.

    Otherwise, try to find any parent `.mdconfig` of `markdown_file`
    with the same rules.

    If there is no `markdown_file` either, the CWD is used to search
    for configuration (see `resolve_parent_config`).
    '''

    if not config_file:
        dir = os.path.dirname(markdown_file) if markdown_file else os.getcwd()
        return resolve_parent_config(dir)

    config = yaml.load(open(config_file, 'r'))
    return resolve_parent_config(os.path.dirname(config_file), [config])


def merge_config(config_list, parse_config):
    '''Merge a config list.

    `parse_config` is a callback to modify a config object on the fly.
    '''

    if not len(config_list):
        return {}

    if not parse_config:
        parse_config = lambda x: x

    config = list(parse_config(config_list.pop(0)).items())

    for i in config_list:
        config += list(parse_config(i).items())

    return dict(config)


class StopParse(Exception):
    pass


class TitleFinder(HTMLParser):
    def feed(self, *args, **kwargs):
        self.title = False
        self.data = None
        self.tag = None

        try:
            super().feed(*args, **kwargs)
        except StopParse:
            pass

        return self.data

    def handle_starttag(self, tag, attrs):
        if len(tag) == 2 and tag[0] == 'h':
            self.title = True
            self.data = ''
            self.tag = tag

    def handle_data(self, data):
        if self.title:
            self.data += data

    def handle_endtag(self, tag):
        if tag == self.tag:
            raise StopParse()


def parse_config(config):
    '''Parse a config object.

    Some known config keys like `layout` are resolved according to the
    config `path` valud.
    '''

    if 'layout' in config:
        if config['layout'] == 'default':
            config['layout'] = None
        else:
            config['layout'] = config['_dir'] + '/' + config['layout']

    return config


def extract_meta(input):
    '''Extract front matter from Markdown input.

    Return a tuple containing the input without front matter
    and the parsed YAML data.
    '''

    if input[0:4] != '---\n':
        return input, {}

    parts = input[4:].split('\n---\n', 2)

    if len(parts) != 2:
        return parts[0], {}

    return parts[1], yaml.load(parts[0])


def resolve_meta(meta, input):
    '''Resolve the meta directory.

    If given input file name is `None`, use the CWD.
    '''

    if input:
        meta['_dir'] = os.path.abspath(os.path.dirname(input))
    else:
        meta['_dir'] = os.getcwd()

    return meta


def main():
    args = docopt(__doc__, version='1.0')

    input = file_or_def(args['<input>'], sys.stdin).read()
    input, meta = extract_meta(input)

    if 'extend' in meta and not meta['extend']:
        config_list = []
    else:
        config_list = resolve_config(args['--config'], args['<input>'])

    config_list.append(resolve_meta(meta, args['<input>']))
    config = merge_config(config_list, parse_config)

    # Default extensions
    extensions = [
        'extra',
        'headerid',
        'smarty',
        'toc',
    ]

    if 'smarty' in config and not config['smarty']:
        extensions.remove('smarty')

    if 'codehilite' in config and config['codehilite']:
        extensions.append('codehilite')

    # Extension configurations
    extension_configs = {k: [] for k in extensions}

    def proxy(name, extension, extension_name):
        if name in config and extension in extension_configs:
            tuple = extension_name, config[name]
            extension_configs[extension].append(tuple)

    proxy('codehilite_linenums', 'codehilite', 'linenums')
    proxy('header_level', 'headerid', 'level')
    proxy('header_anchorlink', 'toc', 'anchorlink')
    proxy('header_permalink', 'toc', 'permalink')
    proxy('toc_title', 'toc', 'title')

    content = markdown(input, extensions=extensions,
                       extension_configs=extension_configs,
                       output_format='html5')

    config['content'] = content

    if 'title' not in config:
        config['title'] = TitleFinder().feed(config['content'])

    if args['--layout']:
        config['layout'] = args['--layout']
    elif 'layout' not in config:
        config['layout'] = None

    layout = file_or_def_io(config['layout'], DEFAULT_LAYOUT).read()
    print(pystache.render(layout, config), end='')


if __name__ == '__main__':
    main()
