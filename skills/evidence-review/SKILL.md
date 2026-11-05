---
name: evidence-review
description: >-
  Review a code change against its spec and the repo's own conventions, and
  report only findings you have proven: reproduced bugs, unmet requirements,
  code nothing needs, and broken house rules, ending in a PASS or FIX verdict.
disable-model-invocation: true
---

# Evidence Review

The reader of this review is a maintainer who will act on every line of it.
A false or misaligned finding costs them more than a missed nit: they chase it,
lose trust, and start skimming. So optimize for signal. Report only what you
have shown to be true, and say plainly when nothing survived. No findings is
better than bad findings.

The bar is not "tests pass". It is: would this repo's maintainer stand behind
the change as is?

## Inputs

- **Spec:** use the one you are given, or a PR description already in hand.
  Don't go looking for one. With no spec, review for BUG and CONVENTION only,
  since MISSING and UNNECESSARY are judged against the spec.
- **Change:** the given diff, branch, PR, or commit range; otherwise the
  current branch against its merge-base with main, plus uncommitted changes.
- **House rules:** `REVIEW.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, or
  similar maintainer-written files, if present.

Do not edit source files. You may write tests to prove a finding; list each one
you wrote in the report so the maintainer can keep or delete it.

## The four kinds of finding

1. **BUG:** wrong behavior for an input or state that can actually occur,
   including side effects on callers, stored data, or external systems.
2. **MISSING:** something the spec requires that is absent, stubbed, or only
   partly wired up (for example, implemented but unreachable from the entry
   point the spec names).
3. **UNNECESSARY:** code, options, abstractions, or dependencies the spec did
   not ask for and nothing in the change needs.
4. **CONVENTION:** a break from a written house rule, or from the way this
   repo already solves the same problem.

Everything else is out of scope: style, naming, formatting, comments,
"consider" or "might" suggestions, hypothetical future needs, and anything a
linter or type checker already enforces. Problems the change did not introduce
are out of scope too, unless the change makes them reachable or worse.

## What counts as evidence

Each finding needs evidence the maintainer can check in a minute. Your
confidence is not evidence, and neither is code that merely looks wrong.

- **BUG:** a test or command you ran, with the exact command, the actual
  result, and the expected one. When running is truly impossible (needs
  production, real hardware, or a timing window you cannot force), give a
  step-by-step trace from a concrete input through file:line to the wrong
  result, and mark the finding **traced, not run**. A trace with a gap is not
  evidence.
- **MISSING:** the spec line quoted, plus what you ran or read that shows the
  gap.
- **UNNECESSARY:** the location, plus a search showing nothing in the change or
  spec uses it. "No test fails without it" is weak on its own, because the code
  may simply be untested.
- **CONVENTION:** the house rule quoted, or two existing places in the repo
  that do it the established way. Your preference is not a convention.

## How to work

1. **Map the change.** Read the diff, then the callers and callees of every
   changed function. Many real bugs live where the new code meets the old.
2. **List the checks.** Write down each spec requirement and each house rule
   that applies. This is the checklist MISSING and CONVENTION come from.
3. **Exercise, don't read.** Verify each suspected bug and each requirement by
   running it: a focused test, a script, or the CLI. "The code looks like it
   handles this" does not verify it.
4. **Probe the edges** of changed code with the inputs that apply: empty,
   boundary, invalid, repeated, concurrent, partial failure, and existing data
   written by the old version.
5. **Attack your own findings.** For each one, look for the reason it is wrong:
   a guard upstream, a caller that never passes that input, a spec line that
   allows it. Drop what does not survive. Most first-draft findings should not.
6. **If already merged,** drop anything a later commit fixed.
7. **Be honest about coverage.** If you could not verify some part (too large,
   no way to run it, missing credentials), name it under *Not verified*. Never
   imply you checked what you did not.

## Output

Use this shape and nothing else. No summary of the change, no praise, no
general remarks: the maintainer already knows what the change is.

```text
Verdict: PASS | PASS (partial) | FIX
High-risk: <paths touched, or "none">

[BUG | MISSING | UNNECESSARY | CONVENTION] one-line statement
Where: file:line (for MISSING, the entry point the spec names)
Evidence: command and output, test name, spec line, or rule
Impact: what breaks, for whom

Not verified: <parts you could not check, or omit>
Tests written: <paths, or omit>
```

- **PASS** means nothing survived and nothing important went unchecked. That
  is a good result; do not pad it with minor findings to look thorough.
- **PASS (partial)** means nothing survived, but a spec requirement or
  high-risk path is under *Not verified*.
- **FIX** means at least one finding follows.
- **High-risk** lists touched paths in auth, payments, migrations, public
  APIs, infra, secrets, and similar. Review these yourself, whatever the
  verdict.

Order findings by impact: data loss, security, and wrong results first, then
unmet requirements, then convention breaks, then unnecessary code. Report at
most seven, since a longer list buries the ones that matter. If more survived,
add one line saying how many lower-impact findings you left out.
