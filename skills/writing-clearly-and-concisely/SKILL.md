---
name: writing-clearly-and-concisely
description: Use when writing or editing prose humans will read—blog posts, social media posts, documentation, READMEs, announcements, explanations, reports, commit messages, error messages, or UI text. Applies Steven Pinker's classic style and curse-of-knowledge remedies so readers outside your head can follow, and strips the hype and filler that make text read as AI-written.
---

# Writing Clearly and Concisely

Unclear writing usually comes from the curse of knowledge: the writer forgets the reader doesn't know what they know. Write for a smart, curious outsider who never saw the Slack thread, the design doc, or the code.

## Write for the outsider

1. **Define each term where it first appears**, or swap it for a plain word.
2. **Explain mechanisms the reader has only heard named.** "Rebuilds files whose content hash changed" needs a line saying the hash changes when the file's bytes change.
3. **Trace one concrete example through the whole explanation**: a specific payment, request, or user, with real or clearly illustrative values.
4. **Include the steps that feel obvious.** They're the ones the reader is missing.
5. **Describe things by what they do**, not by their role in your system: "send the request again; the server drops duplicates," not "hit the idempotency path."
6. **Finish the reader's job.** A workaround must fully work; a limitation needs its consequence and what to do about it.

## Say what you know, and only that

- **Open with the point**, not "This page covers…".
- **Keep the source's facts separate from your guesses.** Don't fill a gap with a plausible detail; mark it as an assumption or an open question.
- **Hedge only a real doubt**, and name the doubt.
- **Call each thing by one name.** A new word signals a new thing.
- **State what is true** rather than what isn't: "the config loads once, at startup," not "the config isn't loaded at runtime."
- **Name the concrete thing**, not a metaconcept: "the process runs out of memory," not "memory-usage issues." Turn zombie nouns back into verbs: "perform an optimization" → "optimize."

## Sentences

- Start with what the reader already knows and end with what's new; the end carries the emphasis. Use the passive when it keeps the topic first, but not when it hides an actor the reader needs: "mistakes were made."
- Keep the subject near its verb and the verb near its object.
- Show how sentences relate with *because, so, but, for example, then*. Arguments need sentences, not bullets.

## Cut hype and filler

Specifics beat adjectives. For each "seamless," "powerful," "game-changer," scene-setting opener, or rhetorical hook, write the fact that made you reach for it, or delete the sentence. Don't format two facts as a table, bold every term, or put headings on a short post. When editing someone else's draft, cut claims nothing backs up and tell the author what you cut so they can restore it with evidence.

For blog and social posts, or when reviewing a draft for AI tells, load `signs-of-ai-writing.md`. Swapping a flagged word for a synonym doesn't help; fix the sentence behind it.

## Before you finish

Reread the draft as the outsider:

1. Would they know every term and abbreviation?
2. Is there a concrete example near each abstraction?
3. Is every stated fact in the source, with guesses marked as guesses?
4. Is any sentence there to impress rather than inform?

---

Adapted from [joshuadavidthomas/agent-skills](https://github.com/joshuadavidthomas/agent-skills) (MIT). Principles from Steven Pinker, *The Sense of Style* (2014).
