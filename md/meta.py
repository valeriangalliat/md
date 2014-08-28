import os
import yaml


def resolve(meta, file):
    '''Resolve the meta directory.

    This will add a `_dir` key to the `meta` object, containing the
    `file` directory, or the CWD if `file` is falsy.
    '''

    if file:
        meta['_dir'] = os.path.abspath(os.path.dirname(file))
    else:
        meta['_dir'] = os.getcwd()

    return meta


def extract(input, file=None):
    '''Extract front matter from Markdown input.

    Return a tuple containing the input without front matter and the
    parsed YAML data.

    The context directory is resolved using `resolve` with `file` param.
    '''

    # Don't begin with a meta block
    if input[0:4] != '---\n':
        return input, {}

    # Split until meta end block
    parts = input[4:].split('\n---\n', 2)

    # There was no end, ignore the meta block
    if len(parts) != 2:
        return parts[0], {}

    # Actual content without the meta block
    content = parts[1]

    # Parse the meta block as YAML
    meta = yaml.load(parts[0])

    # Resolve the context directory
    meta = resolve(meta, file)

    return content, meta
