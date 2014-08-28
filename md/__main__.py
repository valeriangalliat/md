'''Usage: md [options] [<input>]

Arguments:
  <input>  Input file (`stdin` if not set).

Options:
  -h, --help       Show this screen.
  --version        Show version.
  --config=<file>  Try to find a `.mdrc` (recursing in parent
                   directories) if not set.
  --layout=<file>  Layout file (will override config).
'''

import md
import md.config
import md.meta
import md.title
import pystache
import sys

from docopt import docopt
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


def fdef(arg, default):
    '''Return opened `arg` file or `default` stream.'''
    return open(arg, 'r') if arg else default


def fdefio(arg, default):
    '''Return opened `arg` file or `default` string as a `StringIO`.'''
    return fdef(arg, StringIO(default))


def config_proxy(config):
    '''Generate a `kwargs` for `markdown` according to `config`.'''

    kwargs = {}

    def proxy(name):
        if name in config:
            kwargs[name] = config[name]

    proxy('extensions')
    proxy('extension_configs')
    proxy('output_format')

    return kwargs


def main():
    args = docopt(__doc__, version=md.VERSION)

    # Take `<input>` file param or fallback to `stdin`
    input = fdef(args['<input>'], sys.stdin).read()
    input, meta = md.meta.extract(input, args['<input>'])

    config = md.config.find(args['--config'], args['<input>'], meta)
    kwargs = config_proxy(config)

    # Allow to disable an extension by setting its config to `False`
    if 'extension_configs' in kwargs:
        for k, v in kwargs['extension_configs'].items():
            if not v:
                kwargs['extensions'].remove(k)

    config['content'] = markdown(input, **kwargs)

    if 'title' not in config:
        config['title'] = md.title.find(config['content'])

    if args['--layout']:
        config['layout'] = args['--layout']
    elif 'layout' not in config:
        config['layout'] = None

    layout = fdefio(config['layout'], DEFAULT_LAYOUT).read()
    print(pystache.render(layout, config), end='')


if __name__ == '__main__':
    main()
