# writing-clearly-and-concisely

**Prose a reader outside your head can follow.** Style rules for anything humans will read: documentation, READMEs, blog and social posts, announcements, reports, commit messages, error messages, and UI text.

## The problem

Agent-written prose fails in two ways. It assumes the reader saw the Slack thread, the design doc, and the code, so terms go undefined and the "obvious" steps are missing. And it pads: "seamless", "powerful", a scene-setting opener, a summary that restates the post. Readers recognize the second kind quickly and stop reading.

## What you get

- **Writing aimed at a smart outsider.** Each term is defined where it first appears, mechanisms are explained and not only named, and one concrete example is traced through the whole explanation.
- **The point comes first.** No "This page covers..." openers.
- **Facts kept apart from guesses.** The agent does not fill a gap with a plausible detail. It marks an assumption as an assumption, and hedges only a real doubt.
- **Concrete wording.** One name per thing, "the process runs out of memory" instead of "memory-usage issues", and what is true instead of what is not.
- **Hype replaced by the fact behind it.** For each inflated adjective or rhetorical hook, the agent writes the specific fact that prompted it, or deletes the sentence.
- **A review pass for AI tells.** For blog and social posts, a checklist of the patterns that make text read as machine-written, each with a fix.
- **A final reread as the reader.** Four questions before delivering: are all terms known, is there an example near each abstraction, is every fact from the source, and is any sentence there to impress?

## How to use it

Nothing to type. The skill loads on its own when the agent writes or edits prose for people:

```text
Write the release announcement for v2.
```

```text
Edit this blog draft. It sounds like AI wrote it.
```

## What's inside

`SKILL.md` holds the style rules and the final checklist. `signs-of-ai-writing.md` lists the patterns that mark text as AI-written, with a fix for each.

Adapted from [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills) (MIT). Principles from Steven Pinker, *The Sense of Style* (2014).

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
