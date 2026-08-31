# agent-skills

A curated repository of custom AI agent skills and automation workflows. These skills help agents like Claude Code and OpenAI Codex follow my preferred engineering standards, practices, and workflows.

## Directory Structure

```text
agent-skills/
├── .claude-plugin/
│   └── marketplace.json       # Claude plugin marketplace catalog
├── skills/
│   ├── explain/
│   │   ├── examples/          # One runnable diagram per type
│   │   ├── compile.py         # Deterministic diagram compiler
│   │   ├── reference.md       # Diagram IR field list and rule codes
│   │   └── SKILL.md           # Explains a topic as a self-contained HTML page
│   ├── systems-thinking/
│   │   └── SKILL.md           # Cause-and-effect reasoning for complex problems
│   ├── taskfile/
│   │   └── SKILL.md           # Taskfile creation and optimization guidance
│   └── writing-clearly-and-concisely/
│       ├── elements-of-style/ # Detailed writing reference material
│       ├── SKILL.md           # Clear, concise prose guidelines
│       └── signs-of-ai-writing.md
├── .gitignore                 # Ignored subdirectories and environment metadata
├── LICENSE                    # MIT License
└── README.md                  # Repository overview
```

## Skills

- `explain`: Explains a topic or part of a repository as a self-contained HTML page, with deterministically compiled architecture, workflow, sequence, data-flow, and lifecycle diagrams.
- `systems-thinking`: Analyzes complex problems, root causes, constraints, tradeoffs, and potential side effects.
- `taskfile`: Helps create, modify, and optimize Taskfiles using version 3 syntax.
- `writing-clearly-and-concisely`: Applies practical rules for clear, concise prose and avoids common AI writing patterns.

## Getting Started

These skills are packaged as a Claude Code plugin marketplace, allowing them to be loaded and managed natively.

### Installing in Claude Code

#### 1. Add the Marketplace

Add the public GitHub repository:

```bash
/plugin marketplace add itsmostafa/agent-skills
```

#### 2. Install the Plugin

Install the `agent-skills` plugin from the marketplace:

```bash
/plugin install agent-skills@itsmostafa
```

### Adding New Skills

To add a new skill to this repository:

1. Create a new directory inside `agent-skills/skills/` (e.g. `agent-skills/skills/new-skill/`).
2. Add a `SKILL.md` file inside that directory with YAML frontmatter containing `name` and `description`:
   ```yaml
   ---
   name: new-skill
   description: Brief description of when to use this skill.
   ---
   # New Skill Title
   Instructions go here...
   ```
3. Register the new skill path in `.claude-plugin/marketplace.json` under the `skills` list:
   ```json
   "skills": [
     "./skills/explain",
     "./skills/systems-thinking",
     "./skills/taskfile",
     "./skills/writing-clearly-and-concisely",
     "./skills/new-skill"
   ]
   ```

## License

This project is licensed under the [MIT License](LICENSE).
