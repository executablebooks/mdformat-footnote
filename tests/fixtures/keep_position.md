Single footnote stays at its source position
.
Para one.[^a]

[^a]: Definition A.

Para two.
.
Para one.[^a]

[^a]: Definition A.

Para two.
.

Multiple footnotes each stay near their own reference
.
Para one.[^a]

[^a]: Definition A.

Para two.[^b]

[^b]: Definition B.
.
Para one.[^a]

[^a]: Definition A.

Para two.[^b]

[^b]: Definition B.
.

Definition before its reference stays in place
.
[^early]: Defined early.

Para references it here.[^early]
.
[^early]: Defined early.

Para references it here.[^early]
.

Nested footnote body stays at its own source position
.
Body text.[^a]

[^a]: First, references another.[^b]

[^b]: Second.
.
Body text.[^a]

[^a]: First, references another.[^b]

[^b]: Second.
.
