---
name: explain
description: Explain any topic simply for a newcomer — a concept, a system, a process, or part of a codebase — and save it as an HTML page with compiled architecture, workflow, sequence, data-flow, and lifecycle diagrams. Use when the user types /explain <topic>.
disable-model-invocation: true
---

# Explain

Explain the topic for someone seeing it for the first time, in plain terms. No filler.
The output is one self-contained HTML file under `~/explain/`.

Diagrams are **compiled, not drawn**. You describe what a diagram means; `compile.py`
computes every pixel. Never hand-write `<svg>` for structure, and never write coordinates,
`viewBox`, or path data.

Topic: $ARGUMENTS

## Steps

1. **Research.** Ground every claim in a source you actually checked: files in the repo,
   docs, or pages you read. If the topic is code, read the code.

2. **Draft the prose** to `~/explain/<topic-slug>/doc.draft.html` — plain HTML, no CSS, no
   JS. Where a picture beats a paragraph, put a placeholder alone on its own line:

       {{diagram: pipeline.architecture.json}}

   Skip the diagram when the prose already says it.

3. **Write one JSON per placeholder** beside the draft, named `<name>.<type>.json`, with
   semantics only. See `reference.md` for fields and a worked example per type. When
   explaining code, cite it with `src: "path/to/file.py:42"`; the path is checked against
   `--root`.

4. **Compile** with `compile.py` from this skill's directory
   (`${CLAUDE_PLUGIN_ROOT}/skills/explain/compile.py` when the plugin root is set):

       python3 <this skill dir>/compile.py ~/explain/<topic-slug>/doc.draft.html [--root <repo>]

   `--root` is only needed when diagrams cite `src`. It writes `index.html` beside the
   draft. Keep the draft and JSONs so the page can be regenerated.

5. **Fix by rule code.** A non-zero exit lists every problem with its fix. Edit the JSON
   (shorten a label, move a node's `row`, correct a `src`, split the diagram) and re-run
   until clean.

6. **Report** the output path.

## Rules

- **Labels are printable ASCII**: ≤48 chars for nodes, ≤32 for edges, ≤91 for titles.
- **One idea per diagram**, six to twelve nodes. Split rather than crowd.
- **Width is capped at 960px**; length is free. On `E_TOO_WIDE`, shorten labels in the
  widest rank or split the diagram. Sequences scroll sideways instead; keep them to three
  or four participants.
- **Omit `rank` and `row`** unless the default layout reads badly. Then hint every node or
  none, and keep connected nodes on different ranks.
- **Mark loops and retries** with `"back": true`.
- **No JS, no CDN, no network.** The page must open offline.

## Charts

The compiler handles structure, not numbers. For a bar or line chart, hand-write inline
`<svg>` in the draft; the compiler leaves it alone. Style it yourself: a `font-family`,
`fill:currentColor`, width near 900px, and ~16px text to match the prose.
