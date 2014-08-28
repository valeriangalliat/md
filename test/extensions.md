---
extensions:
    - extra
    - headerid
    - smarty
    - toc

extension_configs:
    toc:
        marker: '{{toc}}'
        permalink: true
---

{{toc}}

Hello world!
============

The above header should have an ID and be present in the TOC.

*[TOC]: Table Of Contents

"Some smarty quotes 'here'."

Here
:   Is a definition list.
With
:   Multiple items.

| Table | Baby |
| ----- | ---- |
| Cell  | Cell |

```
Some fenced code block!
```
