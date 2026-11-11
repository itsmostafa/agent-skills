# explain

**Get a newcomer-friendly explainer page for any topic, with diagrams that are compiled instead of drawn.** Point it at a concept, a process, or part of your codebase and it saves one self-contained HTML file you can open offline or send to a teammate.

## The problem

Ask an agent to explain a system and you get a wall of text in the terminal that is gone when the session ends. Ask for a diagram and you get hand-written SVG with overlapping boxes and clipped labels. Neither helps the person joining your team next week.

## What you get

- **A page built for limited attention.** A TL;DR that gives the whole answer in one to three sentences, why it matters, one analogy (and where it breaks), then sections whose headings are the takeaways. Skimming the headings alone teaches the topic.
- **Five diagram types, laid out by a compiler.** Architecture, workflow, sequence, data-flow, and lifecycle. The agent describes what the diagram means in JSON, and `compile.py` computes every position. It checks labels, widths, overlaps, and references, and names the fix for each problem. Bar and line charts are the exception: the agent still writes those as inline SVG.
- **Claims grounded in sources.** The agent reads the code or docs before writing. Diagram nodes can cite `path/to/file.py:42`, and the compiler checks that the path exists.
- **A file that works anywhere.** One HTML file with no JavaScript, no CDN, and no network requests.
- **Pages you can regenerate.** The draft and diagram JSON are kept beside the output, so you can edit and recompile.

## How to use it

This skill runs only when you ask for it:

```text
/explain how our auth token refresh works
```

In pi, use `/skill:explain`. The page is saved to `~/explain/<topic-slug>/index.html`. The compiler needs `python3`.

## What's inside

| File | Purpose |
| --- | --- |
| `SKILL.md` | The steps, the writing rules, and the diagram rules. |
| `compile.py` | Turns the draft and diagram JSON into the final page. |
| `reference.md` | Diagram fields, rule codes, and a worked example per type. |
| `examples/` | One runnable diagram per type, plus a demo draft. |

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
