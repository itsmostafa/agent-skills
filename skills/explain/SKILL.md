---
name: explain
description: Explain a topic or part of the repository simply for someone new to the codebase and save it as an HTML file, with deterministically compiled architecture, workflow, sequence, data-flow, and lifecycle diagrams. Use when the user types /explain <topic>.
---

# Explain

Explain the topic for someone seeing it for the first time. Plain terms, grounded in the
real repo, no filler. The output is one self-contained HTML file under `~/explain/`.

Diagrams are **compiled, not drawn**. You describe what a diagram means; `compile.py`
computes every pixel. Never hand-write `<svg>` for structure, and never write coordinates,
`viewBox`, or path data anywhere.

Topic: $ARGUMENTS

## Steps

1. **Research.** Read the actual code. Every claim traces back to a file you opened.

2. **Draft the prose** to `~/explain/<topic-slug>/doc.draft.html` — plain HTML, no CSS, no
   JS. Where a picture beats a paragraph, put a placeholder alone on its own line:

       {{diagram: pipeline.architecture.json}}

   Skip the diagram when the prose already says it.

3. **Write one JSON per placeholder**, beside the draft, named `<name>.<type>.json`.
   Supply semantics only. Cite real code with `src: "path/to/file.py:42"` — the whole path
   is checked against the repo, and the box prints `file.py:42` with the full path in its
   tooltip. See `reference.md` for the field list and a worked example per type.

4. **Compile.** `compile.py` sits in this skill's own directory — use that absolute path
   (`${CLAUDE_PLUGIN_ROOT}/skills/explain/compile.py` when the plugin root is set).

       python3 <this skill dir>/compile.py ~/explain/<topic-slug>/doc.draft.html --root <repo>

   `--root` is the repo being explained, which is what `src` paths resolve against — not
   the folder the draft lives in. Writes `index.html` beside the draft. Keep the draft and
   the JSONs; they are how the page gets regenerated.

5. **Fix by rule code.** A non-zero exit prints every problem at once, each with the
   semantic fix. Change the **JSON** — move a node to a different `row`, shorten a label,
   correct a `src` line, split a crowded diagram. Never answer a failure with coordinates;
   the format has nowhere to put them. Re-run until it exits clean.

6. **Report** the output path.

## Rules

- **Labels are printable ASCII**, ≤48 chars for nodes, ≤32 for edges. Width is pinned to
  the character count, which non-ASCII breaks — so it is rejected rather than guessed at.
- **One idea per diagram.** Six to twelve nodes. Split rather than crowd.
- **Diagrams share the prose margins.** A graph is capped at the 960px column and never
  scaled down, so `E_TOO_WIDE` means real editing: shorten the longest labels in the
  widest rank, or split the diagram. Ranks run *down* the page, so length is free and
  width is not.
- **Sequences are the exception.** Participants sit side by side, so a wide one scrolls
  sideways inside the column instead of shrinking. Three or four participants fit; more
  is a scroll, and usually two diagrams.
- **Omit `rank` and `row` first.** The compiler stacks ranks down the page by dependency
  depth, packs each rank in declaration order, and slides it under the boxes that feed
  it, so a child sits below its parent. That is usually right. Add hints
  only where the default reads badly, and all-or-nothing: every node gets a `rank`, or
  none does.
- **Edges must connect different ranks.** Auto-layout guarantees this; if you hint ranks
  by hand and two connected nodes land on the same one, give one a different rank.
- **Mark retries and loops** with `"back": true` so they route outside the diagram body.
- **No JS, no CDN, no network.** The file has to open offline.

## Charts

The compiler does structure, not numbers. For a bar or line chart of real figures from the
repo, hand-write inline `<svg>` in the draft as before — that stays allowed, and the
compiler leaves it alone.

It gets none of the compiled styling. Set your own `font-family`, `fill:currentColor`,
a width near 900px, and text at prose size (~16px) — chart text smaller than the
paragraphs around it reads as a mistake.

## Reference

`reference.md` — full IR field list, every rule code with its fix, and one worked example
per diagram type. `examples/` holds those examples as runnable files.
