# itsmostafa agent skills

**An opinionated set of agent skills, curated from how I work.** These are the engineering standards and workflows I use every day, packaged for Claude Code, OpenAI Codex, and pi: simpler code, reviews backed by evidence, clean PRs, and clear explanations.

[![License: MIT](https://img.shields.io/github/license/itsmostafa/agent-skills)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/itsmostafa/agent-skills?style=social)](https://github.com/itsmostafa/agent-skills/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/itsmostafa/agent-skills)](https://github.com/itsmostafa/agent-skills/commits/main)
![Works with Claude Code, Codex, pi](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20pi-blue)

```text
            ┌──────────────────────────┐
            │      agent-skills        │
            │  skills/<name>/SKILL.md  │
            └────────────┬─────────────┘
                         │ one install
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
  ┌────────────┐   ┌──────────────┐   ┌──────────┐
  │Claude Code │   │ OpenAI Codex │   │    pi    │
  └────────────┘   └──────────────┘   └──────────┘
        same standards, every agent, every repo
```

## Why This Exists

**The problem:** Out of the box, coding agents over-engineer. They add dependencies you didn't need, write "looks good to me" reviews with no proof, produce messy commit histories, and pad prose with filler. You end up repeating the same corrections in every session, in every repo, for every agent.

**The solution:** agent-skills packages those corrections once, as plain Markdown skills the agent loads on demand. Install the plugin and every agent you use follows the same engineering standards, with no per-project prompt files to maintain.

## Quickstart

Pick your agent and run one install:

```bash
# Claude Code
/plugin marketplace add itsmostafa/agent-skills
/plugin install agent-skills@itsmostafa

# OpenAI Codex
codex plugin marketplace add itsmostafa/agent-skills
codex plugin add agent-skills@itsmostafa

# pi
pi install git:github.com/itsmostafa/agent-skills
```

Then get your first result in three steps:

1. Restart your agent so it picks up the new skills.
2. Open any repository with uncommitted changes.
3. Run `/create-pr` (or `/skill:create-pr` in pi) and watch it split your work into conventional commits and open a PR.

## What You Get

| Skill | What it gives you |
| --- | --- |
| `minimalist` | Smaller diffs and fewer dependencies: the agent questions the need first (YAGNI), then reaches for the standard library and native platform features before writing custom code. |
| `evidence-review` | Code reviews you can trust: only findings backed by a reproduced bug, an unmet requirement, or a broken repo convention. No speculative nitpicks. |
| `create-pr` | A release-ready PR in one command: changes grouped into conventional commits, pushed to a feature branch, with a release-please friendly description. |
| `explain` | Onboarding docs on demand: any topic or part of your codebase becomes a self-contained HTML page with compiled architecture, workflow, sequence, data-flow, and lifecycle diagrams. |
| `systems-thinking` | Better decisions on hard problems: cause-and-effect reasoning that surfaces root causes, constraints, tradeoffs, and side effects before you commit to a fix. |
| `writing-clearly-and-concisely` | Prose people actually finish reading: Pinker-based style rules that cut filler, hype, and the telltale signs of AI-written text. |
| `readme-marketer` | READMEs that convert visitors into users: a clear hook, a fast quickstart, and features framed as outcomes. (It wrote this page.) |
| `taskfile` | Working Taskfiles on the first try: expert guidance on Taskfile v3 syntax, dependencies, variables, includes, watching, and migrating from Make. |

## Installation Details

### Claude Code

```bash
/plugin marketplace add itsmostafa/agent-skills
/plugin install agent-skills@itsmostafa
```

### OpenAI Codex

Codex reads the same `.claude-plugin/marketplace.json` catalog, so the install id matches Claude Code:

```bash
codex plugin marketplace add itsmostafa/agent-skills
codex plugin add agent-skills@itsmostafa
```

Verify with `codex plugin list`. Pull later changes with:

```bash
codex plugin marketplace upgrade itsmostafa
```

### pi

Install the repository as a [pi](https://pi.dev) package:

```bash
pi install git:github.com/itsmostafa/agent-skills
```

Add `-l` to install for the current project only. Project packages load once the project is trusted. Skills appear on the next `pi` start as `/skill:<name>`.

## Repository Layout

```text
agent-skills/
├── .claude-plugin/
│   └── marketplace.json       # Plugin catalog for Claude Code and Codex
├── skills/
│   ├── create-pr/             # Conventional commits + release-please PR
│   ├── evidence-review/       # Evidence-backed code review
│   ├── explain/               # HTML explainers with a diagram compiler
│   │   ├── examples/          # One runnable diagram per type
│   │   ├── compile.py         # Deterministic diagram compiler
│   │   └── reference.md       # Diagram IR field list and rule codes
│   ├── minimalist/            # YAGNI, stdlib first
│   ├── readme-marketer/       # README rewrites
│   ├── systems-thinking/      # Cause-and-effect reasoning
│   ├── taskfile/              # Taskfile v3 guidance
│   └── writing-clearly-and-concisely/
├── LICENSE
└── README.md
```

Every skill lives in its own directory with a `SKILL.md` entry point.

## Contributing

Have a workflow you keep re-explaining to your agent? Turn it into a skill.

1. Create `skills/new-skill/SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: new-skill
   description: Brief description of when to use this skill.
   ---
   # New Skill Title
   Instructions go here...
   ```
2. Register it in `.claude-plugin/marketplace.json` under the `skills` list:
   ```json
   "skills": [
     "./skills/create-pr",
     "...",
     "./skills/new-skill"
   ]
   ```
3. Open a pull request. Issues and suggestions are welcome too.

If these skills save you a few corrections a day, consider [starring the repo](https://github.com/itsmostafa/agent-skills) so others can find it.

## License

[MIT](LICENSE)
