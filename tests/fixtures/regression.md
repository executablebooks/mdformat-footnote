Issue 7: footnote ref inside footnote without body reference
.
[^a]: lorem
[^c]: ipsum [^a]
.
[^a]: lorem
.


Issue 7: with body reference
.
Body refs [^c]

[^a]: lorem
[^c]: ipsum [^a]
.
Body refs [^c]

[^c]: ipsum [^a]

[^a]: lorem
.


Issue 8: nested footnote refs
.
[^a]: Lorem. [^b]

[^b]: Ipsum.

A [^b]
.
A [^b]

[^b]: Ipsum.
.


Issue 22: nested in admonition
.
# Document

| Color |
| ------ |
| R [^1] |
| G [^2] |
| B [^3] |

```{tip}
| Color |
| ------ |
| C [^4] |
| M [^5] |
| Y [^6] |
```

[^1]: Red

[^2]: Green

[^3]: Blue

[^4]: Cyan

[^5]: Magenta

[^6]: Yellow
.
# Document

| Color |
| ------ |
| R [^1] |
| G [^2] |
| B [^3] |

```{tip}
| Color |
| ------ |
| C [^4] |
| M [^5] |
| Y [^6] |
```

[^1]: Red

[^2]: Green

[^3]: Blue

[^4]: Cyan

[^5]: Magenta

[^6]: Yellow
.


Reference order preserved
.
Text [^b] then [^a]

[^a]: First
[^b]: Second
.
Text [^b] then [^a]

[^b]: Second

[^a]: First
.


Chained nested footnotes
.
Start [^a]

[^a]: References B [^b]
[^b]: References C [^c]
[^c]: Final one
.
Start [^a]

[^a]: References B [^b]

[^b]: References C [^c]

[^c]: Final one
.
