# Signs of AI Writing

Patterns that make blog posts, social posts, and docs read as machine-written. Use this list to review a draft after you write it, not as a list of words to dodge while drafting. Adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (CC BY-SA 4.0), with 2025–2026 research cited inline.

## Core Rules

1. **Fix the cause, not the word.** Each pattern stands in for a missing fact or a claim the writer can't support. Swap the word for a synonym and the emptiness stays; readers learn the new tells quickly ([Geng & Trotta 2025](https://aclanthology.org/2025.findings-acl.657.pdf)). Rewrite around a specific fact, or delete the sentence.
2. **Prefer the specific fact.** Models trade rare, specific detail for common, generic praise: "cut cold builds from 4 minutes to 9 seconds" becomes "dramatically faster builds."
3. **Signs cluster.** Humans use every one of these patterns sometimes. One is harmless; several in a paragraph make the whole piece read as filler.

## Content

| Pattern | Looks like | Fix |
|---|---|---|
| Inflated significance | "a pivotal moment", "a game-changer for teams everywhere", "part of a broader shift" | Say what changed and for whom. Let the reader judge the significance. |
| Promotional tone | "seamless", "robust", "powerful", "blazing fast", "unlock", "supercharge" | Replace with the number, behavior, or example that made you reach for the word. |
| Trailing "-ing" analysis | "…, making it easier than ever to ship", "…, ensuring reliability at scale" | Delete the clause, or turn it into a concrete claim. |
| Vague attribution | "experts agree", "studies show", "many teams find" | Name the source or the team, or drop the claim. |
| Scene-setting openers | "In today's fast-paced world…", "Ever wondered why…?", "Let's dive in" | Open with the news or the point. |
| Formulaic outlook | Closing on "the future is bright", "this is just the beginning", "exciting times ahead" | End on the last useful fact, or a concrete next step for the reader. |
| Summary that restates | "In summary", "Key takeaways", "Conclusion" sections that repeat the body | Cut it. In long docs, keep a summary only if it adds a decision or next step. |

## Language

**AI vocabulary.** Most excess words are verbs and evaluative adjectives ([Kobak et al. 2025](https://www.science.org/doi/10.1126/sciadv.adt3813)), and alignment training amplifies them ([Juzek & Ward](https://arxiv.org/pdf/2508.01930)). Several in one passage is a strong tell: *additionally, align with, boasts, crucial, delve, elevate, emphasizing, enhance, fostering, garner, highlighting, intricate, interplay, key (as an adjective), landscape, leverage, meticulous, navigate (figuratively), nuanced, pivotal, realm, robust, seamless, showcasing, tapestry, testament, underscore, vibrant*.

**Copula avoidance.** *Serves as*, *stands as*, *represents*, *boasts*, *offers*, *features* in place of *is* and *has*.

**Negative parallelism.** Correcting a misconception nobody held: "It's not just X, it's Y", "This isn't about X. It's about Y", "no X, no Y, just Z". State the positive claim directly.

**Rule of three.** Reflexive triplets ("faster, simpler, and more reliable") that make a thin point look thorough. Use the real number of items.

**False ranges.** *From X to Y* with no common scale: "from startups to enterprises, from code to culture." List the items, or save *from…to* for real ranges.

**Stiff synonyms.** Write *use*, *try*, *help*, *start*, *show*, not *utilize*, *endeavor*, *facilitate*, *commence*, *demonstrate*.

**Elegant variation.** Renaming the same thing in each sentence ("the tool… the platform… the solution"). Call each thing by one name.

## Social Posts

- **Hook formulas:** "Here's the thing:", "Unpopular opinion:", "Let that sink in.", "Read that again.", "🧵👇", "I'll be honest…"
- **Broetry:** one short sentence per line, each for dramatic effect.
- **Engagement bait:** "Agree?", "Thoughts?", "Drop a 🔥 if…", "Tag someone who needs this."
- **Humble-brag framing** and lessons nobody asked for: "I was rejected 47 times. Here's what it taught me about leadership."
- **Hashtag and emoji stacks** at the end or on every line.

A good post makes one specific point a reader can use or repeat, in the fewest words that carry it.

## Formatting

- Boldface on every key term, or bold lead-ins on every bullet (`- **Term**: description`) for content that should be prose.
- Bullets for reasoning. Lists suit steps and parallel options; arguments need sentences with *because* and *so*.
- Headings on a 300-word post, headings in Title Case, headings with nothing under them but more headings.
- Tables for two or three facts that fit in a sentence.
- Em dashes where a comma, colon, or parentheses would do. Claude uses about three times the human rate by default ([Freeburg 2026](https://arxiv.org/abs/2603.27006)).
- Emoji on headings or bullets.
- Markdown in places that don't render it (plain-text email, many social platforms, commit messages).

## Leaked Chatbot Text

Keep text addressed to the user out of the finished piece:

- "Here's a draft…", "I hope this helps!", "Would you like me to…", "Feel free to adjust…"
- "It's important to note that…", "It's worth mentioning…"
- Unfilled placeholders: `[Your Name]`, `(add link)`, `2026-xx-xx`
- Letter boilerplate: "I hope this message finds you well"
- Invented specifics dressed as fact: a quote, statistic, customer name, or benchmark the source never gave. When you need one and don't have it, leave a marked placeholder and tell the user.
