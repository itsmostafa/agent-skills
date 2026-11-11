# evidence-review

**Code reviews where every finding comes with proof.** The agent reports only what it has shown to be true: reproduced bugs, unmet requirements, code nothing needs, and broken house rules. It ends with a PASS or FIX verdict.

## The problem

Agent reviews tend to be long lists of "consider renaming this" and "this might fail if". Each speculative item costs you time to chase, and after a few false alarms you start skimming, which is when the real bug gets missed. A review is only useful if you can act on every line of it.

## What you get

- **Findings you can check in a minute.** A bug comes with the exact command that was run, the actual result, and the expected one. When running it is impossible (it needs production or real hardware), the finding carries a step-by-step trace and is marked "traced, not run". A missing requirement comes with the spec line quoted. A convention break comes with the rule quoted, or two places in the repo that already do it the established way.
- **Four kinds of finding and nothing else.** `BUG`, `MISSING`, `UNNECESSARY`, and `CONVENTION`. Style, naming, "consider" suggestions, hypothetical future needs, and anything a linter already enforces are out of scope.
- **Bugs found by running the code.** The agent exercises the change with focused tests and edge inputs (empty, boundary, invalid, repeated, concurrent, partial failure) instead of judging it by reading.
- **Findings that survived an attack.** Before reporting, the agent looks for the reason each finding is wrong, such as an upstream guard or a spec line that allows it, and drops what does not hold up.
- **A clear verdict and honest coverage.** `PASS`, `PASS (partial)`, or `FIX`, at most seven findings ordered by impact, a list of high-risk paths touched (auth, payments, migrations, public APIs), and a *Not verified* section for anything it could not check.

The agent does not edit your source files. If it writes tests to prove a finding, it lists them so you can keep or delete them.

## How to use it

This skill runs only when you ask for it:

```text
/evidence-review
```

In pi, use `/skill:evidence-review`. With no arguments it reviews the current branch against its merge-base with main, plus uncommitted changes. You can also point it at a diff, branch, PR, or commit range, and give it a spec:

```text
/evidence-review PR 42 against the spec in docs/export-spec.md
```

Without a spec it reviews for `BUG` and `CONVENTION` only, since the other two are judged against the spec. House rules are read from `REVIEW.md`, `CONTRIBUTING.md`, `CLAUDE.md`, or `AGENTS.md` if present.

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
