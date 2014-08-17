`md`
====

> Advanced Markdown wrapper.

Overview
--------

`md` is a wrapper around the Python `markdown` module and extensions,
to add a layout around the rendered file, with different levels of
configuration.

### Configuration

A local configuration is the Markdown [meta-data], also known as YAML
front matter. It is always merged with the global configuration, unless
`extend: false` is set.

[meta-data]: https://pythonhosted.org/Markdown/extensions/meta_data.html

A global configuration is a `.mdconfig` YAML file in the nearest
parent directory of the rendered file. `md` will search another parent
`.mdconfig` and merge both files until `extend: false` is set, or the
root is reached.

### Title

The HTML `<title>` can be provided directly with a `title` configuration
key in the Markdown [meta-data], or even in the global configuration,

If no title is found this way, `md` will parse the rendered HTML to
search for a `<h1>` and use its content in `<title>`.

### Layout

The layout can be defined in a `layout` key, targeting a [Mustache] file
relative to the configuration file (or the Markdown file if in the
meta-data).

[Mustache]: https://mustache.github.io/

Dependencies
------------

* `python3`
  * `docopt` <https://pypi.python.org/pypi/docopt2>
  * `markdown` <https://pypi.python.org/pypi/Markdown>
  * `yaml` <https://pypi.python.org/pypi/PyYAML>
  * `pystache` <https://pypi.python.org/pypi/pystache>
