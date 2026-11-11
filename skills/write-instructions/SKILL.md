---
name: "write-instructions"
description: "Write instructions, procedures, runbooks, SOPs and agent prompts where every step has a check and every failure ends safely."
---

# Write Instructions

Write instructions in natural language that a person or an agent can follow as a normal procedure, and that a model or parser can translate into formal statements without guessing. This is not a DSL. It is a controlled natural language: ordinary English with strict sentence patterns.

The underlying model is the Hoare triple: {precondition} step {postcondition}, plus invariants that hold throughout and a goal that defines done.

## When to use

- Writing an SOP, runbook, checklist, deployment plan or incident procedure
- Planning a multi-step agentic task
- Writing instructions an agent will execute and a monitor will check
- Writing instructions a person will follow, especially under pressure
- Converting an existing procedure into a verifiable one

## Sentence patterns

Every claim-bearing sentence uses exactly one of these patterns:

| Pattern | Formal meaning |
|---|---|
| "This is done when [condition]." | Goal |
| "At all times, [condition]." / "Never [action]." | Invariant |
| "Before [step], [condition] must be true." | Precondition |
| "After [step], [condition] is true, checked by [method]." | Postcondition with its checker |
| "If [condition] fails, [action]." | Failure path |

## Rules

1. One claim per sentence.
2. Modal words are strict. *Must*, *never*, *always* mark hard constraints that are verified. *Should* and *may* mark guidance and are not verified.
3. Every postcondition names how it is checked: a tool, command, API, metric or test. If nothing can check it, rewrite it until something can.
4. Name each thing once and reuse that exact name. Do not alternate between "the image" and "the build".
5. Quantify explicitly: *every*, *any*, *none*, *at least N*. Never leave a plural vague.
6. Keep hedges ("probably", "should be fine") out of verifiable sentences. State uncertainty in its own sentence.
7. Every failure path ends in a known safe state: abort, roll back, or escalate to a named person. Never "investigate" with no end state.
8. Preconditions refer only to earlier postconditions or to facts established outside the procedure.
9. Numbers carry units and windows: "under 1% for 10 minutes", not "low".

## Structure

1. Open with the goal and the invariants.
2. Then one short paragraph per step, in order: precondition, action, postcondition with checker, failure path.
3. Keep it readable prose. No tables, symbols or code unless the user asks.

## Example

> This is done when the service runs v2 and health checks pass. At all times, no production data is deleted and no secrets appear in logs.
>
> Before building, all tests must pass. After building, the image digest is recorded, checked by the registry API. If the build fails, abort.
>
> Before the canary, the build must have succeeded. After the canary runs on 5% of traffic, the error rate stays under 1% for 10 minutes, checked by the metrics dashboard. If it doesn't, roll back and abort.
>
> Before promoting, the canary must have passed and the owner must approve. After promoting, health is ok, checked by the health endpoint. If it isn't, roll back.

## Self-check before delivering

- Does every step have a precondition, a postcondition with a named checker, and a failure path?
- Does every failure path end in abort, rollback or escalate?
- Does every precondition point to an earlier postcondition or an external fact?
- Is every invariant something a monitor could check after each step?
- Is the goal checkable, not a judgment call?
- Are names consistent and quantifiers explicit?
- Are all hedges outside verifiable sentences?

Fix any failure before delivering.

## Extraction (when asked to formalize)

If asked to convert the prose to formal form, map each sentence by its pattern into:

```
GOAL  <condition>
INV   <condition>
S<n>  <step>
  PRE  <condition>
  POST <condition>  CHECK <method>
  FAIL <action>
```

Then report any step missing a PRE, POST, CHECK or FAIL as a defect.
