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

Orphan footnote removed while keeping position
.
Body text.[^used]

[^used]: This is used.

[^orphan]: This is never referenced.
.
Body text.[^used]

[^used]: This is used.
.

Orphan footnote kept when keep orphans is also set
.
Body text.[^used]

[^used]: This is used.

[^orphan]: This is never referenced.
.
Body text.[^used]

[^used]: This is used.

[^orphan]: This is never referenced.
.

Fence-referenced footnote not treated as orphan while keeping position
.
Body text.

```text
See [^fenced] in the fence.
```

[^fenced]: Referenced only inside a code fence.
.
Body text.

```text
See [^fenced] in the fence.
```

[^fenced]: Referenced only inside a code fence.
.

Nested-only footnote not treated as orphan while keeping position
.
Body text.[^a]

[^a]: References a nested-only footnote.[^nested]

[^nested]: Never referenced from the body directly.
.
Body text.[^a]

[^a]: References a nested-only footnote.[^nested]

[^nested]: Never referenced from the body directly.
.
