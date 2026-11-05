# Adding Skills

Each skill lives in its own directory under `skills/`, with a `SKILL.md` file as its entry point.

1. Create `skills/new-skill/SKILL.md` with YAML frontmatter containing `name` and `description`:
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
3. Add the skill to the "What You Get" table and the "Repository Layout" tree in the [README](../README.md).
