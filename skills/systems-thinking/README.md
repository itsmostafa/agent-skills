# systems-thinking

**Make the agent find the root cause before it proposes a fix.** A cause-and-effect reasoning method for hard problems: debugging that is not yielding, recurring incidents, architecture decisions, and A-or-B tradeoffs.

## The problem

Agents pattern-match a complex problem to the first plausible fix. The fix usually treats the symptom you reported, so the problem comes back in a different place a week later. On tradeoffs, the default answer is a compromise that leaves both sides worse off. And a fix that sounds right is rarely checked for the new problems it creates.

## What you get

The agent works through up to six questions, using as many as the problem's weight justifies:

1. **Name the goal first.** The outcome the system exists to produce, and the few conditions that must hold. Many arguments about solutions are undetected disagreements about the goal.
2. **Trace the symptom down.** Ask "why does this exist?" one layer at a time, with no skipped steps, until reaching a root cause you can act on. Fix the root and many symptoms disappear together.
3. **Find the constraint.** A system's output is capped by one weakest link at a time. Improving any other link does nothing for the whole.
4. **Validate every "X causes Y".** Eight tests separate a real causal link from a plausible guess. They catch the missing second factor, the independent other cause, and the arrow that points backwards.
5. **Break conflicts instead of compromising.** Find the hidden assumption that makes two requirements look mutually exclusive, and invalidate it.
6. **Stress-test the solution.** Trace forward from the fix to find the side effects it creates, then adjust the fix before committing to it.

In the answer, the agent states the root cause it is targeting, the assumption it invalidated, the side effect it checked, and any causal link it could not verify.

## How to use it

Nothing to type. The skill loads on its own when a problem is more than a lookup or a mechanical edit:

```text
Our deploy queue backs up every Monday. We've added runners twice and it keeps happening. Why?
```

```text
Should we split the monolith now or after the migration?
```

It is skipped for trivial tasks, where heavy analysis would be its own failure.

## What's inside

`SKILL.md` holds the six-step sequence and the anti-patterns it prevents. `references/categories-of-legitimate-reservation.md` holds the eight causal tests in full, with the question each asks and worked examples.

The method is distilled from H. William Dettmer's *The Logical Thinking Process*, the reasoning method of the Theory of Constraints.

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
