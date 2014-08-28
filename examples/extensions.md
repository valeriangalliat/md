---
extensions:
    - extra
    - headerid
    - smarty
    - toc

extension_configs:
    toc:
        permalink: true
---

Hello world!
============

This Markdown file is rendered with [some extensions][extensions].

[extensions]: https://pythonhosted.org/Markdown/extensions/

## Abbreviations

The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium

## Definition lists

Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

## Code blocks

```python hl_lines="1 3"
# This line is emphasized
# This line isn't
# This line is emphasized
```

Other syntaxes [are supported][code-blocks].

[code-blocks]: https://pythonhosted.org/Markdown/extensions/fenced_code_blocks.html

## Footnotes

Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".

## Tables

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

## Header ID

Notice how each header have an `id` attribute, and an anchor at the
end (displayed on hover with the current layout).

Also, see how the Markdown headers were shifted one level down with
configuration!

## SmartyPants

Look carefully how are styled "double quotes", 'simple quotes', ellipses
and [more][smarty]...

[smarty]: https://pythonhosted.org/Markdown/extensions/smarty.html

## Table of contents

It is usually on the top of the page, but I'll dsplay it here.

[TOC]
