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


def main():
    args = docopt(__doc__, version=md.VERSION)

    # Take `<input>` file param or fallback to `stdin`
    input = fdef(args['<input>'], sys.stdin).read()
    input, meta = md.meta.extract(input, args['<input>'])

    config = md.config.find(args['--config'], args['<input>'], meta)

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
        config['title'] = md.title.find(config['content'])

    if args['--layout']:
        config['layout'] = args['--layout']
    elif 'layout' not in config:
        config['layout'] = None

    layout = fdefio(config['layout'], DEFAULT_LAYOUT).read()
    print(pystache.render(layout, config), end='')


if __name__ == '__main__':
    main()
