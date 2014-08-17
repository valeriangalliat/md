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


def resolve_config(config):
    if config:
        return open(config, 'r')

    dir = os.getcwd()
    isroot = False

    while not isroot:
        isroot = dir == '/'

        try:
            return yaml.load(open(dir + '/.mdconfig', 'r'))
        except FileNotFoundError:
            pass

        dir = os.path.dirname(dir)

    return {}


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


def main():
    args = docopt(__doc__, version='1.0')
    config = resolve_config(args['--config'])
    input = file_or_def(args['<input>'], sys.stdin).read()

    md = Markdown(extensions=MARKDOWN_EXTENSIONS)
    config['content'] = md.convert(input)

    meta = md.Meta

    if 'title' in meta:
        meta['title'] = meta['title'][0]

    # Merge meta and config
    config = dict(list(meta.items()) + list(config.items()))

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
