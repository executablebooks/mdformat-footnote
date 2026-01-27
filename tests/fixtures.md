a test
.
This is the input Markdown test,
then below add the expected output.
.
This is the input Markdown test,
then below add the expected output.
.


another test
.
Some *markdown*

* a
* b
- c
.
Some *markdown*

- a
- b

* c
.


Test Footnotes
.
# Now some markdown
Here is a footnote reference,[^1] and another.[^longnote]
[^1]: Here is the footnote.
[^longnote]: Here's one with multiple blocks.

    Subsequent paragraphs are indented to show that they
belong to the previous footnote.

    Third paragraph here.
.
# Now some markdown

Here is a footnote reference,[^1] and another.[^longnote]

[^1]: Here is the footnote.

[^longnote]: Here's one with multiple blocks.

    Subsequent paragraphs are indented to show that they
    belong to the previous footnote.

    Third paragraph here.
.


Empty footnote
.
Here is a footnote reference [^emptynote]

[^emptynote]: 
.
Here is a footnote reference [^emptynote]

[^emptynote]: 
.


Move footnote definitions to the end (but before link ref defs)
.
[link]: https://www.python.org
[^1]: Here is the footnote.

# Now we reference them
Here is a footnote reference[^1]
Here is a [link]

.
# Now we reference them

Here is a footnote reference[^1]
Here is a [link]

[^1]: Here is the footnote.

[link]: https://www.python.org
.

footnote-indentation
.
[^a]

[^a]: first paragraph with
unindented next line.

    paragraph with
    indented next line

    paragraph with
unindented next line

    ```
    content
    ```
.
[^a]

[^a]: first paragraph with
    unindented next line.

    paragraph with
    indented next line

    paragraph with
    unindented next line

    ```
    content
    ```
.


footnote-ref-inside-footnote (issue #7)
.
[^a]: lorem
[^c]: ipsum [^a]
.
[^a]: lorem

[^c]: ipsum [^a]
.


nested-footnote-refs (issue #8)
.
[^a]: Lorem. [^b]

[^b]: Ipsum.

A [^b]
.
A [^b]

[^a]: Lorem. [^b]

[^b]: Ipsum.
.


Footnote in table nested in admonition (issue #22)
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
