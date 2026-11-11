# create-pr

**Turn a pile of uncommitted changes into a reviewable pull request with one command.** The agent groups your work into conventional commits, pushes a feature branch, and opens a GitHub PR whose description release-please can read.

## The problem

At the end of a session you have a working tree with a feature, a bug fix, and some test changes mixed together. The quick way out is one commit called "updates" and a PR with an empty description. Reviewers then have to reconstruct what changed and why, and your changelog tooling has nothing to work from.

## What you get

- **Commits a reviewer can read in order.** Changes are grouped by feature, layer, change type, and scope, then ordered so that reading them oldest-first explains the change: setup, then implementation, then tests and docs.
- **Correct version bumps.** Every commit follows Conventional Commits (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`), and breaking changes get a `!` or a `BREAKING CHANGE:` footer, so release-please picks the right version.
- **No accidental commits to main.** If you are on `main` or `master`, the agent creates a branch named `<type>/<scope>-<short-description>` first.
- **A PR description that is already filled in.** Summary, commit list, changes, breaking changes, test plan, related issues, release notes, and a checklist.
- **Judgment about when not to split.** A small or tightly coupled change stays a single commit.

## How to use it

This skill runs only when you ask for it. With uncommitted changes in your repository, type:

```text
/create-pr
```

In pi, use `/skill:create-pr`. The agent prints the PR URL when it is done.

You need `git` and an authenticated [GitHub CLI](https://cli.github.com) (`gh`).

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
