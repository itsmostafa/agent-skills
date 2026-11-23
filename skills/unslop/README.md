# unslop

**Text that doesn't read as AI-written.** Run `/unslop` on a draft and the agent rewrites it without the patterns that give machine prose away, while it keeps the meaning and the tone.

## The problem

AI drafts share a set of tells: "delve", "pivotal", and "testament", a trailing "ensuring..." phrase, "not just X, but Y", ideas forced into threes, em dashes, bold labels on every line, stacked hedges, and a closing line that could end any document. Readers spot them fast and stop trusting the rest.

## What you get

- **A numbered rule list.** 26 rules, each a single line, such as "Say 'is' or 'has', not 'serves as'" and "One hedge at most". The numbers are stable ids, so you can cite a rule by number.
- **Stock vocabulary removed.** Words like "additionally", "crucial", "leverage", "paradigm", and "north star" become the plain, concrete word.
- **Punctuation and formatting cleaned up.** Periods and commas replace dashes, quotes are straight, headings use sentence case, and decorative emojis and bold are gone.
- **Specific claims.** Vague attributions get a named source or get cut. Adverbs become numbers or stronger verbs. Generic conclusions become specific facts or plans.
- **No chatbot voice.** No "Great question!", no "I hope this helps!", and no "Let me know if...".

## How to use it

Run it with the text or file you want cleaned:

```text
/unslop posts/launch-announcement.md
```

```text
/unslop Fix the summary you just wrote.
```

In pi, use `/skill:unslop`.

The skill only runs when you invoke it. The agent never loads it on its own.

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
