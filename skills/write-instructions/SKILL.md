---
name: "write-instructions"
description: "Write or rewrite instructions that must be followed exactly and checked: SOPs, runbooks, deployment and rollback plans, incident procedures, checklists, and multi-step plans or prompts for AI agents. Each step gets a precondition, a checkable result, and a failure path that ends safely. Use when the user asks for a procedure, runbook, SOP, step-by-step plan or agent instructions, or wants an existing procedure made verifiable, even if they don't name this skill."
---

# Write Instructions

Write instructions in natural language that a person or an agent can follow as a normal procedure, and that a model or parser can translate into formal statements without guessing. This is not a DSL. It is a controlled natural language: ordinary English with strict sentence patterns.

The underlying model is the Hoare triple: {precondition} step {postcondition}, plus invariants that hold throughout and a goal that defines done.

## Sentence patterns

Every claim-bearing sentence uses exactly one of these patterns:

| Pattern | Formal meaning |
|---|---|
| "This is done when [condition]." | Goal |
| "At all times, [condition]." / "Never [action]." | Invariant |
| "Before [step], [condition] must be true." | Precondition |
| "[Imperative action]." | Action |
| "After [step], [condition] is true, checked by [method]." | Postcondition with its checker |
| "If [condition] fails, [action]." | Failure path |

## Rules

1. One claim per sentence.
2. Modal words are strict. *Must*, *never*, *always* mark hard constraints that are verified. *Should* and *may* mark guidance and are not verified.
3. Every postcondition names how it is checked: a tool, command, API, metric or test. If nothing can check it, rewrite it until something can. For a step that needs human judgment, the checker is a named person's recorded sign-off.
4. Name each thing once and reuse that exact name. Do not alternate between "the image" and "the build".
5. Quantify explicitly: *every*, *any*, *none*, *at least N*. Never leave a plural vague.
6. Keep hedges ("probably", "should be fine") out of verifiable sentences. State uncertainty in its own sentence.
7. Every failure path ends in a known safe state: abort, roll back, or escalate to a named person. Never "investigate" with no end state.
8. Preconditions refer only to earlier postconditions or to facts established outside the procedure.
9. Numbers carry units and windows: "under 1% for 10 minutes", not "low".
10. State what happens when an invariant breaks: "If any invariant breaks, [safe state]."
11. Never invent a checker, threshold or person the user did not give. Write `[TBD: what is missing]` in its place and list every TBD at the end.

## Structure

1. Open with the goal and the invariants.
2. Then one short paragraph per step, in order: precondition, action, postcondition with checker, failure path.
3. Keep it readable prose. No tables or symbols unless the user asks. Inline commands in backticks are fine when they are the action or the checker.
4. In an agent prompt, apply the patterns to the procedural parts only. Persona, tone and style guidance stays plain prose using *should* and *may*.

## Example

> This is done when 100% of traffic runs on v2 and the health endpoint returns 200 for 5 consecutive minutes, checked by `curl https://api.example.com/healthz`. At all times, no production table is dropped, checked by the database audit log. At all times, no secret appears in logs, checked by the log scanner. If any invariant breaks, roll back and escalate to Priya Shah.
>
> Before building, every unit test must pass in CI. Build the v2 image. After building, the v2 image digest is in the registry, checked by `crane digest registry.example.com/api:v2`. If the build fails, abort.
>
> Before the canary, the v2 image digest must be in the registry. Route 5% of traffic to v2. After the canary, the v2 error rate is under 1% for 10 minutes, checked by the api-errors dashboard. If the v2 error rate check fails, roll back and abort.
>
> Before promoting, the v2 error rate must be under 1% for 10 minutes. Before promoting, Priya Shah must approve, checked by her sign-off on the release ticket. Route 100% of traffic to v2. After promoting, the health endpoint returns 200 for 5 consecutive minutes, checked by `curl https://api.example.com/healthz`. If the health endpoint check fails, roll back and escalate to Priya Shah.

## Self-check before delivering

- Does every step have a precondition, an action, a postcondition with a named checker, and a failure path?
- Does every failure path end in abort, rollback or escalate?
- Does every precondition point to an earlier postcondition or an external fact?
- Is every invariant something a monitor could check after each step, and is there a path for when one breaks?
- Is the goal checkable, not a judgment call?
- Are names consistent and quantifiers explicit?
- Are all hedges outside verifiable sentences?
- Is every unknown marked `[TBD: ...]` and listed at the end, with nothing invented?

Fix any failure before delivering.

## Extraction (when asked to formalize)

If asked to convert the prose to formal form, map each sentence by its pattern into:

```
GOAL  <condition>
INV   <condition>
S<n>  <step>
  PRE  <condition>
  DO   <action>
  POST <condition>  CHECK <method>
  FAIL <action>
```

Then report any step missing a PRE, DO, POST, CHECK or FAIL as a defect, and any TBD as an open item.
