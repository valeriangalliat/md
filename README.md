`md`
====

> Advanced Markdown wrapper.

Overview
--------

`md` is a wrapper around the Python `markdown` module and extensions,
to add a layout around the rendered file, and provide a global
configuration (with extend and override support).

The global configuration is a `.mdconfig` YAML file in the nearest
parent directory of the rendered file. If te configuration contains
`extend: true`, `md` will search another parent `.mdconfig` and merge
both files until there is no `extend` or the root is reached.

The HTML `<title>` can be provided directly with a `title` configuration
key in the Markdown [meta-data], or even in the global configuration,

[meta-data]: https://pythonhosted.org/Markdown/extensions/meta_data.html

If no title is found this way, `md` will parse the rendered HTML to
search for a `<h1>` and use its content in `<title>`.

Dependencies
------------

* `python3`
  * `docopt` <https://pypi.python.org/pypi/docopt2>
  * `markdown` <https://pypi.python.org/pypi/Markdown>
  * `yaml` <https://pypi.python.org/pypi/PyYAML>
  * `pystache` <https://pypi.python.org/pypi/pystache>
