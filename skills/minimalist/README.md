# minimalist

**Smaller diffs and fewer dependencies.** The agent asks whether the code needs to exist before writing it, then reaches for what your codebase, the standard library, and the platform already provide.

## The problem

Ask an agent for a cache and you get a custom cache class, a config file, and a new dependency. Ask for a bug fix and you get a guard in the one caller the ticket named, while the sibling callers stay broken. Every extra line is something you have to review now and maintain later.

## What you get

- **A fixed order of questions before any code.** Does this need to exist? Is it already in this codebase? Does the standard library do it? Does a native platform feature cover it (`<input type="date">` over a picker library, a database constraint over app code)? Does an installed dependency solve it? Can it be one line? Only then does the agent write the minimum code that works.
- **Root-cause bug fixes.** The agent greps every caller before editing. One guard in the shared function is a smaller diff than a guard in every caller.
- **No speculative structure.** No interface with one implementation, no factory for one product, no config for a value that never changes, no scaffolding "for later".
- **A note on what was skipped.** Each answer ends with a line like "skipped the custom cache class, add when `lru_cache` measurably falls short", so you can ask for the fuller version when you need it.
- **One check left behind.** Non-trivial logic gets the smallest test that fails if the logic breaks: one test in your existing test setup, or a bare `assert` if the repo has none.
- **Limits on the laziness.** Input validation at trust boundaries, error handling that prevents data loss, security measures, accessibility basics, and anything you explicitly requested are never simplified away.

## How to use it

Nothing to type. The skill loads on its own before the agent writes, edits, fixes, refactors, or reviews code, and stays in effect for the rest of the session. It also triggers when you ask for the simplest way or complain about over-engineering:

```text
Add a cache for these API responses.
```

```text
This PR feels bloated. What can we cut?
```

If you want the full version of something, say so and the agent builds it without arguing.

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
