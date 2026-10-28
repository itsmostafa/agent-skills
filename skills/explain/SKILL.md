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
computes every pixel. For anything the compiler can build, never hand-write `<svg>`, and
never write coordinates, `viewBox`, or path data.

Topic: $ARGUMENTS

If the topic is empty, take it from the conversation; if there is nothing to take, ask.

## Steps

1. **Research.** Ground every claim in a source you actually checked: files in the repo,
   docs, or pages you read. If the topic is code, read the code.

2. **Draft the prose** to `~/explain/<topic-slug>/doc.draft.html` — plain HTML, no CSS, no
   JS — following **Writing for attention** below. Where a picture beats a paragraph, put a
   placeholder alone on its own line:

       {{diagram: pipeline.architecture.json}}

   Skip the diagram when the prose already says it.

3. **Skim the draft as the reader would.** Read only the `<h1>`, the TL;DR, and the
   `<h2>`s. If that alone doesn't teach the topic, fix the headings before going on.

4. **Write one JSON per placeholder** beside the draft, named `<name>.<type>.json`, with
   semantics only. See `reference.md` for fields, rule codes, and a worked example per
   type. When explaining code, cite it with `src: "path/to/file.py:42"`; the path is
   checked against `--root`.

5. **Compile** with `compile.py` from the base directory given when this skill was invoked:

       python3 <skill base dir>/compile.py ~/explain/<topic-slug>/doc.draft.html [--root <repo>]

   `--root` is only needed when diagrams cite `src`. It writes `index.html` beside the
   draft. Keep the draft and JSONs so the page can be regenerated.

6. **Fix by rule code.** A non-zero exit lists every problem with its fix. Edit the JSON
   (shorten a label, move a node's `row`, correct a `src`, split the diagram) and re-run
   until clean.

7. **Report** the output path.

## Writing for attention

Every rule here either cuts what the reader must hold in mind or makes the idea stick.
Working memory is the bottleneck, so the numbers below are targets that protect it, not
caps to contort prose around.

**Page shape**, in this order:

1. **`<h1>`**: the topic as a plain question or claim.
2. **TL;DR**: one to three sentences that give the whole answer. A reader who stops here
   still got it.
3. **Why it matters**: one or two sentences on what problem this solves or what the reader
   can do once they get it. Attention follows a visible payoff.
4. **Analogy**: one everyday comparison, flagged as an analogy, then one line on where it
   breaks, so the reader keeps the useful part and drops the wrong part.
5. **Sections**: one idea each. Make every `<h2>` the section's takeaway as a sentence
   ("Tokens expire after an hour", not "Expiry"), so skimming the headings alone teaches
   the topic.
6. **Recap**: three to five bullets, each a full claim. Restating the core is what makes
   it stick.

**Sentences and paragraphs**

- One idea per sentence; aim under 20 words. No nested clauses or double negatives:
  each one makes the reader hold half a thought while parsing the rest.
- Paragraphs of one to three sentences. Use a list when there are three or more parallel
  items or ordered steps.
- Active voice, common words, literal language. Define each term on first use, and
  introduce no more than about three new terms per section; each new term is one more
  thing to hold.
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

## Diagram rules

The compiler checks labels, widths, overlaps, and references, and names the fix for each.
These are the judgment calls it can't make:

- **One idea per diagram**, up to about twelve nodes. Split rather than crowd.
- **Keep sequences to three or four participants.** They scroll sideways past that.
- **Omit `rank` and `row`** unless the default layout reads badly. Then hint every node or
  none, and keep connected nodes on different ranks.
- **Mark loops and retries** with `"back": true`.
- **No JS, no CDN, no network.** The page must open offline.

## Charts

The compiler handles structure, not numbers. For a bar or line chart, hand-write inline
`<svg>` in the draft; the compiler leaves it alone. Style it yourself: a `font-family`,
`fill:currentColor`, width near 900px, and ~16px text to match the prose.
