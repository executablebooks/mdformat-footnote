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
