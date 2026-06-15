---
name: git-workflow
description: Personal git workflow and best practices for structured commits, branching, and repository hygiene. Use when creating branches, writing commit messages, or resolving git conflicts.
---

# Git Workflow Skill

A clean, reliable git workflow to maintain structured commits and branch hygiene in software projects.

## Commit Message Convention

Follow the Conventional Commits specification for all commits:

- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation-only changes
- `style:` Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `perf:` A code change that improves performance
- `test:` Adding missing tests or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools and libraries such as documentation generation

### Format

```text
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Example:
```text
feat(auth): add MFA support via authenticator apps
```

## Branching Strategy

1. **Main Branch:** `main` (production-ready code)
2. **Feature Branches:** `feature/issue-description` or `feat/short-description`
3. **Bugfix Branches:** `bugfix/issue-description` or `fix/short-description`
4. **Hotfix Branches:** `hotfix/urgent-patch`

## Common Commands

### Creating a Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b feat/your-feature
```

### Squashing Commits before PR Merges
```bash
git rebase -i main
```

### Safely Amending the Last Commit (Unpushed Only)
```bash
git commit --amend --no-edit
```
