# The Sense of Style: Guidelines

Guidelines for prose that people read, drawn from Steven Pinker's *The Sense of Style* (2014). Each guideline follows from how readers process language. The reason is given with each one; use it to decide edge cases.

## 1. Classic Style

Treat prose as a window onto the subject. You have seen something the reader hasn't; point them at it. Assume the reader is smart and simply hasn't seen it yet. Present the finished view, not the route you took to reach it. Technical writing succeeds when the reader walks away seeing the mechanism, and classic style keeps attention on the mechanism.

- Talk about the subject, not the text. Cut "In this section we will discuss..." and "As noted above...". Where the reader needs a signpost, use a question they actually have: "Why does the cache miss here?"
- Talk about the subject, not the field: "A cache trades memory for latency," not "Researchers have taken many approaches to caching."
- Hedge only where you have a specific doubt, and say what the doubt is. Unexplained "somewhat," "arguably," "to some extent," and "it seems that" weaken every claim they touch. State what you believe and qualify it once, where it matters.
- Open with content. Skip "This is a complex topic..."; the reader will judge that.
- Use words straight. If a word needs scare quotes to distance you from it, pick a better word.
- Turn zombie nouns back into verbs, because nominalizations hide the action: "perform an optimization of" → "optimize"; "the implementation of caching resulted in a reduction of latency" → "caching cut latency."
- State the concrete idea instead of wrapping it in a metaconcept (*level, issue, approach, framework, process, model, perspective, context*): "memory-usage issues" → "the process runs out of memory."
- Name the actor when the reader needs to know who acts. "Mistakes were made" hides it.

## 2. The Curse of Knowledge

This is the main cause of unclear expert writing: once you know something, it is hard to imagine not knowing it, so you write for a reader who already shares your context. Write for a specific reader instead: smart, curious, and outside the team.

- Define each term and abbreviation at first use, or replace it with a plain word. Terms you use constantly feel ordinary to you; the reader never learned them.
- Unpack chunks. An abstract label like "the reconciliation phase" compresses ideas the reader has no unpacked version of; say what happens.
- Describe things by what they are or do, not by their role in your system: "send the same request again; the server ignores duplicates," not "hit the idempotency endpoint."
- Include the steps that feel obvious. They are obvious only to someone who already knows them, and they are the ones the reader most needs.
- Put a concrete example right before or right after each abstraction.
- Before finishing, reread the draft as that outside reader: mark each term they wouldn't know and each step they would have to fill in.

## 3. Syntax

The reader rebuilds the structure of each sentence from a string of words, left to right. Write so they can do it without backtracking.

- Avoid garden paths, where early words invite a wrong parse ("The old man the boat"). Reread each sentence as a stranger would.
- Keep the subject near its verb and the verb near its object. Move long clauses out of the gap.
- Put short phrases first and long, heavy phrases last, where the reader isn't holding anything open.
- Start with what the reader already knows and end with what's new. The end of a sentence carries the emphasis.
- Use the passive when it keeps the topic in subject position or puts known information first: "The request hits the load balancer. It is then routed to a worker." Use the active when the passive would hide an actor the reader needs.
- Express parallel ideas in parallel structure.

## 4. Coherence

The reader should always know what the text is about and how each sentence connects to the one before.

- Open with the point, then give background.
- Call each thing by one name. Once it is "the worker," keep it "the worker," not "the process," "the job runner," or "the daemon." Readers assume a new word means a new thing.
- Mark how sentences relate with connectives such as *because, so, but, for example, in contrast, then*, so the reader knows whether a sentence elaborates, contrasts, explains a cause, or comes next in sequence.
- State what is true rather than what isn't. Negations take longer to process and leave the reader unsure what holds: "The config isn't loaded at runtime" → "The config loads once, at startup."
- In a long document, a roadmap helps when it describes the content ("First the data model, then the sync protocol"), not the document.

## 5. Usage Rules

Usage rules are conventions. Follow the ones that prevent ambiguity or whose breach looks careless (subject-verb agreement, dangling modifiers, *its/it's*). Ignore superstitions such as never splitting an infinitive or never starting a sentence with *And*.

## Checklist

1. Am I pointing the reader at the subject, or talking about my text or my field?
2. Would a smart outsider know every term I use?
3. Is there a concrete example near each abstraction?
4. Have I turned zombie nouns back into verbs?
5. Does each sentence start with the familiar and end with the new?
6. Do I call each thing by one name throughout?
7. Is every hedge tied to a real, stated doubt?
