---
name: explain
description: Explain any topic simply for a newcomer, in a form an ADHD reader can grasp fast and retain — a concept, a system, a process, or part of a codebase — and save it as an HTML page with compiled architecture, workflow, sequence, data-flow, and lifecycle diagrams. Use when the user types /explain <topic>.
disable-model-invocation: true
---

# Explain

Explain the topic for someone seeing it for the first time, in plain terms. No filler.
Write for a reader with ADHD: little working memory to spare, and attention that leaves
the moment the payoff is unclear. They should get the idea fast and still remember it
tomorrow. The output is one self-contained HTML file under `~/explain/`.

Diagrams are **compiled, not drawn**. You describe what a diagram means; `compile.py`
computes every pixel. Never hand-write `<svg>` for structure, and never write coordinates,
`viewBox`, or path data.

Topic: $ARGUMENTS

## Steps

1. **Research.** Ground every claim in a source you actually checked: files in the repo,
   docs, or pages you read. If the topic is code, read the code.

2. **Draft the prose** to `~/explain/<topic-slug>/doc.draft.html` — plain HTML, no CSS, no
   JS — following **Writing for attention** below. Where a picture beats a
   paragraph, put a placeholder alone on its own line:

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

## Writing for attention

Every rule here either cuts what the reader must hold in mind or makes the idea stick.

**Page shape**, in this order:

1. **`<h1>`**: the topic as a plain question or claim.
2. **TL;DR**: one to three sentences that give the whole answer. A reader who stops here
   still got it.
3. **Why it matters**: one or two sentences on what problem this solves or what the reader
   can do once they get it.
4. **Analogy**: one everyday comparison, flagged as an analogy, then one line on where it
   breaks.
5. **Sections**: one idea each. Make every `<h2>` the section's takeaway as a sentence
   ("Tokens expire after an hour", not "Expiry"), so skimming the headings alone teaches
   the topic.
6. **Recap**: three to five bullets, each a full claim.

**Sentences and paragraphs**

- One idea per sentence; aim under 20 words. No nested clauses or double negatives.
- Paragraphs of one to three sentences. Use a list when there are three or more parallel
  items or ordered steps.
- Active voice, common words, literal language. Define each term on first use, and
  introduce no more than three new terms per section.
- Example first, then the rule. A concrete case gives the abstraction something to hold on
  to.
- Bold the one phrase per section the reader must remember, and only that one. If you bold
  more, nothing stands out.
- Make numbers relatable: compare them to something familiar ("about the size of a photo").

**Keep the main path short.** Put caveats, edge cases, and history in
`<details><summary>Go deeper: …</summary>…</details>` so the main path stays a few minutes'
read. Cut whatever doesn't serve the TL;DR.

**Pair each diagram with its sentence.** Put the placeholder right after the sentence it
illustrates, and have that sentence say what to look at ("Follow the token from left to
right").

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
