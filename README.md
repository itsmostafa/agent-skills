# My Personal Skills

A private, curated repository of custom AI agent skills and automation workflows. These skills are designed to make agents like Claude Code and OpenAI Codex more capable and aligned with my preferred engineering standards, practices, and workflows.

## Directory Structure

```text
├── .claude-plugin/
│   └── marketplace.json    # Claude plugin marketplace catalog
├── skills/
│   ├── git-workflow/       # Custom skill for git workflows
│   │   └── SKILL.md        # Git workflow instructions & guidelines
│   └── writing-clearly-and-concisely/
│       └── SKILL.md        # Clear, concise prose guidelines
├── .gitignore              # Ignored subdirectories & environment metadata
└── README.md               # Repository overview
```

## Getting Started

These skills are packaged as a Claude Code plugin marketplace, allowing them to be loaded and managed natively.

### Installing in Claude Code

#### 1. Add the Marketplace
You can add this repository as a local plugin marketplace:

```bash
/plugin marketplace add /Users/hackmini/Projects/skills
```

Or once pushed to a private/public GitHub repository:

```bash
/plugin marketplace add itsmostafa/skills
```

#### 2. Install the Plugin
Install the `personal-skills` plugin from the marketplace:

```bash
/plugin install personal-skills@personal-skills
```

### Adding New Skills

To add a new skill to this repository:

1. Create a new directory inside `skills/` (e.g. `skills/new-skill/`).
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
     "./skills/git-workflow",
     "./skills/writing-clearly-and-concisely",
     "./skills/new-skill"
   ]
   ```

## License

Private Repository - All Rights Reserved
