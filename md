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
from markdown import Markdown


DEFAULT_LAYOUT = '''<!DOCTYPE html>
<html{{#lang}} lang="{{lang}}"{{/lang}}>
<head>
<meta charset="utf-8">
<title>{{title}}</title>
</head>
<body>
{{#h1}}
<h1>{{title}}</h1>
{{/h1}}
{{{content}}}
</body>
</html>
'''

MARKDOWN_EXTENSIONS = [
    'extra',
    'headerid',
    'meta',
    'smarty',
    'toc',
]


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
    elif 'extend' not in config_list[0] or not config_list[0]['extend']:
        return config_list

    try:
        path = dir + '/.mdconfig'
        parent = yaml.load(open(path, 'r'))
        parent['dir'] = os.path.dirname(path)
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

        try:
            super().feed(*args, **kwargs)
        except StopParse:
            pass

        return self.data

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.title = True
            self.data = ''

    def handle_data(self, data):
        if self.title:
            self.data += data

    def handle_endtag(self, tag):
        if tag == 'h1':
            raise StopParse()


def parse_config(config):
    '''Parse a config object.

    Some known config keys like `layout` are resolved according to the
    config `path` valud.
    '''

    if 'layout' in config:
        config['layout'] = config['dir'] + '/' + config['layout']

    return config


def main():
    args = docopt(__doc__, version='1.0')


    input = file_or_def(args['<input>'], sys.stdin).read()

    md = Markdown(extensions=MARKDOWN_EXTENSIONS)
    content = md.convert(input)

    meta = {k: v[0] for k, v in md.Meta.items()}

    if 'dir' not in meta:
        if args['<input>']:
            meta['dir'] = os.path.abspath(os.path.dirname(args['<input>']))
        else:
            meta['dir'] = os.getcwd()

    config_list = resolve_config(args['--config'], args['<input>'])
    config_list.append(meta)

    config = merge_config(config_list, parse_config)
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
