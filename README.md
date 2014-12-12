md
==

> Advanced Markdown wrapper.

Overview
--------

md is a wrapper around the Python `markdown` module and [extensions],
to add a layout around the rendered file, with different levels of
configuration.

[extensions]: https://pythonhosted.org/Markdown/extensions/

### Configuration

A local configuration is the Markdown meta-data, also known as YAML
front matter. It is always merged with the global configuration, unless
`extend: false` is set.

The meta-data is processed as pure YAML and wrapped with `---` above
and below. It is not parsed with the [meta-data extension][meta-data].

[meta-data]: https://pythonhosted.org/Markdown/extensions/meta_data.html

A global configuration is a `.mdrc` YAML file in the nearest
parent directory of the rendered file. md will search another parent
`.mdrc` and merge both files until `extend: false` is set, or the
root is reached.

### Title

The HTML `<title>` can be provided directly with a `title` configuration
key in the Markdown meta-data, or even in the global configuration,

If no title is found this way, md will parse the rendered HTML to
search for the first header and use its content in `<title>`.

### Layout

The layout can be defined in a `layout` key, targeting a [Mustache] file
relative to the configuration file (or the Markdown file if in the
meta-data). If you set it to `default`, the default layout is used
(thus overriding any parent `layout` without needing to stop the extend
chain).

[Mustache]: https://mustache.github.io/

Dependencies
------------

* `python3`
  * `docopt` <https://pypi.python.org/pypi/docopt>
  * `markdown` <https://pypi.python.org/pypi/Markdown>
  * `yaml` <https://pypi.python.org/pypi/PyYAML>
  * `pystache` <https://pypi.python.org/pypi/pystache>

Installation
------------

Just put the `bin/md` executable in your `PATH` after installing
the required dependencies.

Examples
--------

Watch the [`examples`](examples) directory.
