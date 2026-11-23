# technical-writing

**Docs a tired engineer understands on the first read.** A layered standard for docs, RFCs, READMEs, PR descriptions, and commit messages. Each layer handles one level: document structure, sentences, instructions, and syntax.

## The problem

Agent-written docs mix a tutorial, a reference table, and a design rationale on one page. The sentences are vague ("schema changes can cause issues"), the steps hide a warning after the command it guards, and "it" or "this" could point at three different things. The reader has to read twice to find what to do.

## What you get

- **One mode per document (Diátaxis).** The agent picks tutorial, how-to, reference, or explanation before it writes, and splits the page when the content mixes modes.
- **Sentences written to the reader (Google developer style).** Second person, present tense, active voice, commands for instructions, and headings that state the point in sentence case.
- **Instructions that load one at a time (Simplified Technical English).** One instruction per sentence, a length limit near 20 words, and every warning placed before the step it guards.
- **No sentence with two readings (Global English).** Every pronoun points at one thing, each thing keeps one name, and idioms and Latin abbreviations go.
- **Rules for repo writing.** PR bodies a reviewer reads in under a minute, logs and metric tables linked instead of pasted, real paths, and counts that are true at the commit that lands them.

## How to use it

Run it when you write or review a doc:

```text
/technical-writing Rewrite docs/deploy.md as a how-to guide.
```

```text
/technical-writing Review the description for this PR.
```

In pi, use `/skill:technical-writing`.

The skill only runs when you invoke it. The agent never loads it on its own.

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
