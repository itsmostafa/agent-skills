---
name: systems-thinking
description: >-
  A rigorous cause-and-effect thinking discipline for reasoning about non-trivial
  problems, drawn from the Theory of Constraints Logical Thinking Process. Use it
  BEFORE proposing a fix, plan, or recommendation whenever a problem is more than a
  simple lookup or mechanical edit: debugging that isn't yielding, "why does X keep
  happening", root-cause or incident analysis, architecture and design decisions,
  tradeoffs and either/or conflicts ("should we do A or B"), evaluating whether a
  proposed solution will actually work, refactors, strategy, or any recurring/systemic
  issue. It helps you separate symptoms from root causes, find the one constraint that
  limits the outcome, validate every causal claim with eight logical tests, break
  conflicts instead of splitting the difference, and stress-test a solution for side
  effects before committing. Reach for it even when the user hasn't named a "method" —
  if you're about to explain a cause or recommend an action on a hard problem, run this
  first.
---

# Systems Thinking - The Logical Thinking Process

A discipline for thinking about hard problems, distilled from H. William Dettmer's *The Logical Thinking Process* (the Theory of Constraints reasoning method). Its whole purpose is to stop you from doing the thing that feels productive and is usually wrong: pattern-matching a complex problem to the first plausible fix.

## The one idea to hold onto

**What you are handed is almost always a symptom, and the fix that first comes to mind almost always treats the symptom.** Real leverage lives one or more causal layers down, at a *root cause*, and often at a single *constraint* that limits the whole system. Rigor here is not ceremony — it is how you avoid solving the wrong problem convincingly.

> *"Complex problems have simple, easy-to-understand wrong answers."*

## When to run it

Run this before you commit to a diagnosis, a plan, or a recommendation on any problem that isn't trivial. You do **not** need to draw the formal trees the book describes — that's for facilitated group analysis. What transfers to everyday reasoning is the *sequence of questions* below and the *validation checklist*. Use as much of it as the problem's weight justifies: a quick either/or decision might only need steps 4–5; a nasty recurring failure deserves all six.

Skip it for lookups, single mechanical edits, or questions with one uncontested answer. Applying heavy causal analysis to a trivial task is its own failure mode.

## The sequence

### 1. Name the destination before you optimize
You cannot call anything a "problem" or an "improvement" without a standard to measure against. Before diagnosing, get explicit about:
- **The goal** — the actual outcome the system exists to produce (decided by its owner, not by you).
- **Necessary conditions** — the few non-negotiables that must hold to reach the goal (safety, correctness, a budget, a deadline, trust). These are constraints on the solution space, *not* the goal itself — keep them distinct, because confusing a necessary condition for the goal quietly narrows every option you'll consider.

*Why:* an hour spent making the destination precise saves days of well-executed work in the wrong direction. Most "we disagree on the solution" arguments are really undetected disagreements about the goal.

### 2. Treat the presenting problem as a symptom; trace it down
The thing you were told about is an **Undesirable Effect (UDE)** — a *visible indication* that something is wrong, not the wrong thing itself. Apply the **"So what?" / "Why?" test**: for each UDE, ask "why does this exist? what is its *direct and unavoidable* cause?" Keep going one honest layer at a time — no skipped steps (a jump that hides intermediate steps is a "long arrow" and usually hides a faulty assumption).

Stop when you reach a **critical root cause**: the lowest level of cause that is *still within your sphere of influence to change*. Two tests must both hold — it's near the bottom of the causal chain, **and** you can actually act on it.

*Why:* a few root causes typically account for the large majority (~70%) of the surface symptoms. Fix the root and many symptoms vanish at once; fix a symptom and it regrows. Watch specifically for **reinforcing loops** (a "death spiral" where an effect feeds back to strengthen its own cause) — break those first, because they don't resolve on their own.

### 3. Find the constraint — the one weakest link
A system is a chain: its output is limited by exactly **one** weakest link at a time. Improving any other link — however satisfying, however measurable — does nothing for the whole. So ask: *what single thing, if it stays as it is, caps the outcome no matter what else I improve?* Concentrate there.

*Why:* effort spread evenly across everything is effort spent mostly on non-constraints, i.e. wasted. And beware the deeper trap: **the system optimum is not the sum of the local optima.** Making every component individually "efficient" usually de-optimizes the whole — the real problems often live in the *interfaces between parts*, not the parts.

### 4. Validate every causal claim (the sharpest tool in the box)
Any time you assert "X causes Y" — in your own reasoning, in the user's premises, in a diagnosis you're about to act on — run it through the **Categories of Legitimate Reservation**: eight specific tests that separate a real cause-and-effect relationship from a plausible-sounding guess.

The eight, in brief:
1. **Clarity** — Do I actually understand the claim, with no missing intermediate steps?
2. **Entity Existence** — Is each statement a single, complete, real, verifiable idea?
3. **Causality Existence** — Read aloud "*If* X, *then* Y." Does it truly hold?
4. **Cause Insufficiency** — Is X *alone* enough, or is an unstated **AND**-factor also required?
5. **Additional Cause** — Could an independent **OR**-cause produce Y all by itself? (If so, removing X won't fix Y.)
6. **Cause-Effect Reversal** — Is the arrow backwards? Is X actually just how I *know* about Y, not why Y happens?
7. **Predicted Effect Existence** — If X were true, some *other* effect must also exist. Is it there? (The strongest way to confirm or kill a claim about an invisible cause.)
8. **Tautology** — Am I using the effect as the proof of the cause? ("They played badly — how do you know? — they lost.")

**Read `references/categories-of-legitimate-reservation.md` for how to apply each test, the exact question to ask, and worked examples.** These are worth internalizing; #4, #5, and #6 catch the errors that most often survive casual reasoning. Two shortcuts to keep in mind always: **correlation is not causation**, and **necessary is not sufficient**.

### 5. When there's a conflict, break it — don't compromise
Hard problems often stall on an either/or: A vs. B, speed vs. safety, this team's need vs. that team's. The instinct is to split the difference. Resist it — *"a compromise is a solution with which everybody is equally unhappy."*

Instead, lay the conflict out as: both sides actually want the same **objective**; each pursues a different **requirement**; each requirement seems to demand a conflicting **action**. Now hunt the hidden **assumption** on each link — the unstated "because…" that makes the two feel mutually exclusive. Say each one in extreme terms ("we can *never*…", "there's *absolutely no way*…") so the shaky ones jump out. The conflict is not real; it rests on an assumption that is invalid or no longer true. **Invalidate one assumption and the forced choice dissolves.** The breakthrough idea that does this — an action or condition that lets you satisfy a requirement *without* paying its supposed cost — is an *injection*. Aim for win-win (both sides get more than they expected), not a truce.

*Why:* most persistent conflicts persist precisely because everyone accepts the false assumption underneath them. Attacking assumptions is where genuinely new options come from.

### 6. Bench-test your solution before you commit — run the "negative branch"
Before you recommend or implement a fix, deliberately try to find how *your own solution* creates new problems. Trace forward: "if I do this, then… and combined with [reality that's already true], then…" — and look for the point where the chain turns sour. This is the **negative branch**, and it is the antidote to *"the chief cause of problems is solutions."*

If you find one, you don't necessarily abandon the fix — you **trim the branch** by adding a further adjustment that neutralizes the side effect, then re-check what follows. A solution you've stress-tested this way is worth far more than a clever idea you haven't.

*Why:* every change has unintended effects as well as intended ones; the law of unintended consequences has killed more solutions than bad intentions ever did. Five minutes of "what could this break?" is the cheapest insurance you can buy. (This step works standalone — use it even on small everyday decisions.)

## How to show your work

You don't have to narrate all six steps. But when you deliver a diagnosis or recommendation on a substantive problem, make the *load-bearing* reasoning visible:
- State the **root cause** you're targeting and why it (not the symptom) is the lever.
- If you resolved a conflict, name the **assumption you invalidated**.
- Flag the **negative branch** you checked and how you trimmed it.
- If a causal link is doing heavy lifting and you're not certain of it, say which **reservation** (from step 4) is unresolved rather than papering over it.

Honesty about an unverified causal link beats a confident story. *"It's better to be approximately correct than precisely incorrect."*

## Anti-patterns this skill exists to prevent

| Reflex | What to do instead |
|--------|-------------------|
| Fixing the first symptom you can reach | Trace down to a root cause you can actually act on (step 2) |
| Improving whatever's easiest to improve | Find and work the constraint (step 3) |
| "X causes Y" because they move together | Run the CLR; correlation isn't causation (step 4) |
| Splitting the difference on a tradeoff | Surface and break the hidden assumption (step 5) |
| Shipping the clever fix immediately | Trace its negative branch first (step 6) |
| Optimizing every part for its own sake | Remember: system optimum ≠ sum of local optima (step 3) |

## Reference files
- `references/categories-of-legitimate-reservation.md` — the eight logical tests in full: the exact question each asks, how to apply it, worked examples, and the verbal shorthand. Read this whenever you need to actually validate (or refute) a cause-and-effect claim.
