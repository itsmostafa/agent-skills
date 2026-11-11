# write-instructions

**Procedures in which every step can be checked, written for a person or an AI agent to follow.** Each step says what must be true before it starts, how to confirm it worked, and what to do if it didn't. Use it for runbooks, standard operating procedures (SOPs), deployment and rollback plans, incident procedures, checklists, and multi-step agent prompts.

## The problem

A typical runbook step reads "deploy the new version and make sure it looks healthy". It doesn't say what has to be in place first, what "healthy" means, or what to do when it isn't. A person fills those gaps with judgment at 3am. An agent fills them with a guess.

## What you get

The skill writes each step as a short paragraph with four parts, each a sentence in a fixed pattern. Here is the step that sends a small share of traffic to a new version, v2, before everyone gets it (a canary):

> Before the canary, the v2 image digest must be in the registry. Route 5% of traffic to v2. After the canary, the v2 error rate is under 1% for 10 minutes, checked by the api-errors dashboard. If the v2 error rate check fails, roll back and abort.

1. **"Before..." says what must already be true.** Here, the built v2 image has to be in the registry, the store that deploys pull images from. A "before" condition points to the result of an earlier step or to a fact established outside the procedure.
2. **A plain command is the action.** "Route 5% of traffic to v2."
3. **"After..., checked by..." says what result to expect and what measures it.** The checker is a command, API, metric, or test. For a step that needs human judgment, it is a named person's recorded sign-off. If nothing can check a result, the skill rewrites the step until something can. Numbers carry units and a time window: "under 1% for 10 minutes", not "low".
4. **"If... fails, ..." says what to do when the check fails.** Every failure ends in a known state: abort, roll back, or escalate to a named person. "Investigate" with no end state is not allowed.

The procedure opens with two more patterns:

- **The goal:** "This is done when 100% of traffic runs on v2 and the health endpoint returns 200 for 5 consecutive minutes, checked by `curl https://api.example.com/healthz`."
- **Conditions that hold during every step, called invariants:** "At all times, no secret appears in logs, checked by the log scanner." One more sentence says what to do if one breaks: "If any invariant breaks, roll back and escalate to Priya Shah."

Three more writing rules apply to every sentence:

- **Nothing is invented.** If you didn't give a checker, a threshold, or a person, the skill writes `[TBD: what is missing]` in its place and lists every gap at the end.
- **"Must", "never", and "always" mark hard requirements that get checked.** "Should" and "may" mark guidance that doesn't.
- **Each thing has one name.** The procedure doesn't call the same artifact "the image" in one step and "the build" in the next.

In an agent prompt, the patterns apply only to the procedural parts. Persona, tone, and style guidance stay ordinary prose.

You can also ask for a formal outline. The skill converts the prose to a `GOAL` / `INV` / `PRE` / `DO` / `POST` / `CHECK` / `FAIL` listing, reports any step missing a `PRE`, `DO`, `POST`, `CHECK`, or `FAIL` as a defect, and lists every `[TBD]` as an open item.

## How to use it

The skill loads on its own when you ask for a procedure, runbook, SOP, step-by-step plan, or agent instructions, or ask to make an existing procedure verifiable:

It fits each stage of the software development lifecycle:

| Stage | Example request |
|---|---|
| Plan | `Write a step-by-step plan for an agent to migrate the users table to the new schema.` |
| Build | `Write agent instructions for adding an API endpoint, from branch to merged pull request.` |
| Review | `Turn our code review guidelines into a checklist where every item can be verified.` |
| Test | `Write the procedure for running the regression suite before a release.` |
| Release | `Rewrite this deploy checklist so every step can be verified.` |
| Operate | `Write a rollback runbook for the payments service.` |
| Respond | `Write the incident procedure for a database failover.` |

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
