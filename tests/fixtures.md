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


Multiple references to same footnote with subIds
.
First [^1] and second [^1] and third [^1]

[^1]: Shared footnote
.
First [^1] and second [^1] and third [^1]

[^1]: Shared footnote
.


Orphan footnotes (defined but never referenced)
.
Referenced [^used]

[^orphan]: This is never referenced

[^used]: This is used

[^another-orphan]: Also unused
.
Referenced [^used]

[^orphan]: This is never referenced

[^used]: This is used

[^another-orphan]: Also unused
.


Chained nested footnote references (A references B, B references C)
.
[^a]: References B [^b]

[^b]: References C [^c]

[^c]: Final one

Start [^a]
.
Start [^a]

[^a]: References B [^b]

[^b]: References C [^c]

[^c]: Final one
.


Complex mixed ordering with multiple references
.
[^z]: Defined first

[^a]: Defined second

Text [^a] then [^z] then [^a] again
.
Text [^a] then [^z] then [^a] again

[^z]: Defined first

[^a]: Defined second
.


Footnote referenced in body and within another footnote
.
[^x]: Simple

[^y]: Contains [^x] reference

Body [^x] and [^y]
.
Body [^x] and [^y]

[^x]: Simple

[^y]: Contains [^x] reference
.


Deeply nested: footnote in list in footnote
.
[^outer]: List item:
    - Item with [^inner] reference
    - Another item

[^inner]: Inner content

Text [^outer]
.
Text [^outer]

[^outer]: List item:

    - Item with [^inner] reference
    - Another item

[^inner]: Inner content
.


Multiple footnotes in nested structures
.
[^1]: First

[^2]: Second with [^1]

[^3]: Third with [^2] and [^1]

Body: [^3] [^2] [^1]
.
Body: [^3] [^2] [^1]

[^1]: First

[^2]: Second with [^1]

[^3]: Third with [^2] and [^1]
.


Reordering with mixed body and nested references
.
[^c]: Defined first

[^b]: Defined second [^c]

[^a]: Defined third [^b]

Body [^a] [^b] [^c]
.
Body [^a] [^b] [^c]

[^c]: Defined first

[^b]: Defined second [^c]

[^a]: Defined third [^b]
.


Footnotes with same reference appearing in body and definitions
.
[^shared]: Base note

[^wrapper]: Contains [^shared]

First [^shared] in body, then [^wrapper]
.
First [^shared] in body, then [^wrapper]

[^shared]: Base note

[^wrapper]: Contains [^shared]
.


Complex scenario: multiple refs, nesting, and reordering
.
[^z]: Last defined [^a]

[^m]: Middle defined

[^a]: First defined [^m]

Body [^m] [^a] [^z] [^m]
.
Body [^m] [^a] [^z] [^m]

[^z]: Last defined [^a]

[^m]: Middle defined

[^a]: First defined [^m]
.


Footnote in blockquote with nested reference
.
[^inner]: Inner note

[^outer]: Quote:
    > Blockquote with [^inner]

Text [^outer]
.
Text [^outer]

[^inner]: Inner note

[^outer]: Quote:

    > Blockquote with [^inner]
.


Three-level deep nesting
.
[^1]: Level 1

[^2]: Level 2 [^1]

[^3]: Level 3 [^2]

Start [^3]
.
Start [^3]

[^1]: Level 1

[^2]: Level 2 [^1]

[^3]: Level 3 [^2]
.


Mixed orphans and referenced with complex ordering
.
[^used-first]: Used

[^orphan-1]: Never used

[^used-second]: Also used [^used-first]

[^orphan-2]: Also never used

Body [^used-second] [^used-first]
.
Body [^used-second] [^used-first]

[^used-first]: Used

[^orphan-1]: Never used

[^used-second]: Also used [^used-first]

[^orphan-2]: Also never used
.


Footnotes in table cells with cross-references
.
[^1]: First

[^2]: Second [^1]

| Col A | Col B |
| ----- | ----- |
| A [^1] | B [^2] |
.
| Col A | Col B |
| ----- | ----- |
| A [^1] | B [^2] |

[^1]: First

[^2]: Second [^1]
.


Same footnote multiple times in same and different contexts
.
[^repeat]: Repeated note

Para 1: [^repeat] [^repeat]

[^nested]: Has [^repeat] inside

Para 2: [^nested] [^repeat]
.
Para 1: [^repeat] [^repeat]

Para 2: [^nested] [^repeat]

[^repeat]: Repeated note

[^nested]: Has [^repeat] inside
.
