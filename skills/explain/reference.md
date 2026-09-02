# Diagram IR reference

## What you supply, what the compiler owns

You supply **meaning**: which boxes exist, what connects them, and — only if the default
reads badly — a coarse `rank`/`row` integer.

The compiler owns **every pixel**: box sizes, column and row positions, edge routes, label
placement, canvas size, loop routing. There is no field for a coordinate, and any
unrecognised key is a hard error. When a check fails, the fix is always semantic.

## Graph IR

For `architecture`, `workflow`, `dataflow`, and `lifecycle`. All four share one layout
engine and differ only in what you call them.

```json
{
  "type": "architecture",
  "title": "Auth service",
  "nodes": [
    { "id": "api", "label": "API Gateway", "kind": "service",
      "rank": 1, "row": 0, "src": ["src/api/gateway.py:42"] }
  ],
  "edges": [
    { "from": "api", "to": "db", "label": "query" }
  ]
}
```

| Field | Required | Type | Default |
|---|---|---|---|
| `type` | yes | `architecture` \| `workflow` \| `dataflow` \| `lifecycle` | — |
| `title` | no | printable ASCII, 1–91 | none |
| `nodes` | yes | list, ≥1 | — |
| `edges` | no | list | `[]` |

**`nodes[i]`**

| Field | Required | Type | Default |
|---|---|---|---|
| `id` | yes | string, unique | — |
| `label` | yes | printable ASCII, 1–48 | — |
| `kind` | no | `service` \| `store` \| `external` \| `terminal` | `service` |
| `rank` | no | int — stage down the flow | dependency depth |
| `row` | no | int — order across the rank | declaration order |
| `src` | no | string or list of `path` / `path:line` | none |

Ranks stack down the page and rows spread across it, so a long chain costs height, which
is free, and only the widest rank costs width, which the prose column pins. Each rank is
packed as one block in `row` order and slid under the boxes that feed it, so children sit
below their parent rather than on a shared column grid, and the block is then kept inside
the widest rank's extent — no rank can push the diagram wider than that one. `row` orders
a rank; it does not pin an x position.

`src` is validated in full and printed as the file name and line — the directory is in
the box's tooltip, not in its width.

**`edges[i]`**

| Field | Required | Type | Default |
|---|---|---|---|
| `from` | yes | node id | — |
| `to` | yes | node id | — |
| `label` | no | printable ASCII, ≤32 | none |
| `back` | no | bool — route as a loop outside the body | `false` |

`kind` sets colour and the legend swatch; `terminal` also rounds into a pill. Every node
is a rectangle, so a long label always fits.

## Sequence IR

```json
{
  "type": "sequence",
  "title": "Login",
  "participants": [ { "id": "ui", "label": "Browser", "kind": "external" } ],
  "messages": [
    { "from": "ui", "to": "api", "label": "POST /login" },
    { "from": "api", "to": "ui", "label": "200 + JWT", "style": "return" }
  ]
}
```

`title` takes the same 91-char cap as a graph title. `participants[i]`: `id` (req,
unique) · `label` (req, ASCII ≤48) · `kind` · `src`. Needs at least two.

`messages[i]`: `from` (req) · `to` (req) · `label` (ASCII ≤40) ·
`style` (`call` | `return` | `async`, default `call`). Needs at least one.

`from == to` draws a self-call loop. Lane spacing widens automatically so message labels
never collide — no hints needed anywhere in a sequence diagram.

A sequence is the one diagram that is horizontal by nature: its participants cannot be
stacked. Five heads already exceed the prose column, so a wide sequence scrolls sideways
inside it rather than being scaled below prose size. Keep to three or four participants
where the story allows.

## Rule codes

Everything is reported in one pass, then the compiler exits 1 having written nothing.

| Code | Meaning | Fix |
|---|---|---|
| `E_IO` | the file could not be read | check the path |
| `E_JSON_PARSE` | not valid JSON | fix the syntax |
| `E_JSON_DUPKEY` | the same key twice in one object | delete one |
| `E_TYPE_UNKNOWN` | `type` is not one of the five | use a listed type |
| `E_FIELD_MISSING` | a required field is absent | add it |
| `E_FIELD_TYPE` | wrong type (`true` is not an int) | correct the value |
| `E_FIELD_UNKNOWN` | key not in the spec | delete it — this is what stops geometry leaking into the IR |
| `E_ENUM` | bad `kind` or `style` | pick a listed value |
| `E_ID_DUP` | two nodes share an id | rename one |
| `E_EDGE_REF` | edge names a node that doesn't exist | fix the id |
| `E_EMPTY` | no nodes, <2 participants, or no messages | add content |
| `E_EDGE_SAMERANK` | both ends sit at the same rank | give one a different `rank` |
| `E_EDGE_SELF` | a graph edge points at itself | remove it, or use a sequence self-call |
| `E_EDGE_DUP` | the same `from`→`to` twice | delete one |
| `E_EDGE_BACK_FORWARD` | `back: true` on an edge that runs forward | drop `back`, or reverse the edge |
| `E_LABEL_CHARSET` | non-ASCII, empty, or padded label | use plain printable ASCII |
| `E_LABEL_LONG` | label over its cap | shorten it |
| `E_HINT_PARTIAL` | some nodes hint `rank`/`row`, others don't | hint all of them or none |
| `E_ROW_DUP` | two nodes at the same `rank`+`row` | move one to another `row` |
| `E_SRC_FORMAT` | not `path` or `path:line` | use a POSIX relative path |
| `E_SRC_ESCAPE` | absolute, or outside `--root` | cite a file inside the repo |
| `E_SRC_MISSING` | no such file under `--root` | correct the path |
| `E_SRC_LINE` | file is shorter than the cited line | correct the line number |
| `E_LABEL_OVER_NODE` | an edge label lands on a box | shorten the label, or move a node to a different `row` |
| `E_LABEL_OVER_LABEL` | two edge labels collide | shorten one, or move a node |
| `E_TOO_WIDE` | a graph is wider than the 960px prose column | shorten the longest labels in the widest rank, or split it — sequences are exempt and scroll instead |
| `E_PLACEHOLDER_MISSING` | `{{diagram: x.json}}` has no such file | add the file or fix the name |
| `E_PLACEHOLDER_ESCAPE` | `{{diagram: ...}}` points outside the draft directory | keep diagrams beside the draft |

## Worked examples

One runnable file per type in `examples/`, all five wired into a page by
`examples/demo.draft.html`:

| File | Shows |
|---|---|
| `auth.architecture.json` | components and stores, with `src` evidence on two nodes |
| `deploy.workflow.json` | a retry loop via `"back": true` |
| `login.sequence.json` | `return` messages and a self-call |
| `ingest.dataflow.json` | a straight pipeline, no hints at all |
| `order.lifecycle.json` | explicit `rank`/`row` order, plus a loop back to an earlier state |

Rebuild them, and check the whole thing still holds, with:

```bash
python3 compile.py --selftest
```

which compiles every example twice and asserts the output is byte-identical, ASCII-only,
free of overlapping boxes, and free of any edge crossing a node.
