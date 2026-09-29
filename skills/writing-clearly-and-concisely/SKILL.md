---
name: writing-clearly-and-concisely
description: Use when writing or editing prose humans will read—blog posts, social media posts, documentation, READMEs, announcements, explanations, reports, commit messages, error messages, or UI text. Applies Steven Pinker's classic style and curse-of-knowledge remedies so readers outside your head can follow, and strips the hype and filler that make text read as AI-written.
---

# Writing Clearly and Concisely

Most unclear writing isn't clumsy; it's written for a reader who already knows what the writer knows. Steven Pinker calls this the curse of knowledge (*The Sense of Style*, 2014). Fluent prose doesn't cure it, so the steps below target it directly.

## Write for a smart outsider

Picture a specific reader: smart, curious, and outside your team. They never saw the Slack thread, the design doc, or the code.

1. **Define each term where it first appears**, or swap it for a plain word. Abbreviations and internal names feel ordinary to you because you use them daily.
2. **Explain mechanisms the reader has only heard named.** "Only rebuilds files whose content hash changed" means little until you say a hash is a fingerprint of the file's bytes that changes when the contents change.
3. **Trace one concrete example through the whole explanation.** Pick a specific payment, request, or user and follow it step by step, with real or clearly illustrative values. A worked example teaches what a list of abstractions can't.
4. **Include the steps that feel obvious.** They're obvious only to you, and they're the ones the reader is missing.
5. **Describe things by what they do**, not by their role in your system: "send the request again; the server drops duplicates," not "hit the idempotency path."
6. **Finish the reader's job.** A workaround must fully work; a limitation needs its consequence and what to do about it.

## Say what you know, and only that

- **Open with the point.** Skip "This page covers…" and "In this post we'll explore…"; start with the subject.
- **Keep the source's facts separate from your guesses.** When notes, a diff, or a brief leave a gap, don't fill it with a plausible-sounding detail. State what the source supports; mark the rest as an assumption or list it as an open question for the reader to check.
- **Hedge only a real doubt**, and name the doubt.
- **Call each thing by one name.** A new word signals a new thing.
- **State what is true** rather than what isn't: "the config loads once, at startup," not "the config isn't loaded at runtime."
- **Turn zombie nouns back into verbs**: "perform an optimization" → "optimize."

## Cut hype and filler

Specifics beat adjectives. For each "seamless," "powerful," "game-changer," scene-setting opener, joke, or rhetorical hook, find the fact that made you reach for it and write that instead, or delete the sentence. Don't format two facts as a table, bold every term, or put headings on a short post. When editing someone else's draft, cut claims nothing backs up ("lightweight," "fast," "works with your tooling"), then tell the author what you cut so they can restore it with evidence.

For blog and social posts, or when reviewing a draft for AI tells, load `signs-of-ai-writing.md` (~1,300 tokens): it lists the patterns (hook formulas, broetry, inflated significance, AI vocabulary, negative parallelism) with fixes. Swapping a flagged word for a synonym doesn't help; fix the sentence behind it.

## Before you finish

Reread the draft as that outside reader:

1. Would they know every term and abbreviation?
2. Is there a concrete example near each abstraction, and one traced end to end in anything that explains a system?
3. Is every stated fact in the source, with guesses marked as guesses?
4. Is any sentence there to impress rather than inform?

## Reference

`sense-of-style.md` (~1,300 tokens) explains each principle with examples, plus sentence-level guidance (given before new, keeping related words together, when the passive helps). Load it for long documents, or when editing someone else's draft and you need to explain a change. Short text like commit messages and error messages doesn't need it.
