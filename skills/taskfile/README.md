# taskfile

**Get a working `Taskfile.yml` without reading the docs first.** Guidance for [Taskfile](https://taskfile.dev), the YAML task runner, covering version 3 syntax, common patterns, and the mistakes that cost the most time.

## The problem

A Taskfile that looks right can still fail in small ways: a variable written `{{VAR}}` instead of `{{.VAR}}` never expands, and a build without `sources` and `generates` reruns every time. You end up debugging the task runner instead of using it.

## What you get

- **Correct version 3 syntax.** Variables and their precedence, dynamic variables from command output, environment variables, platform-specific commands, preconditions, loops, includes, and file watching.
- **Tasks that skip work already done.** `sources` and `generates` (or a custom `status` check) so a build runs only when its inputs changed.
- **Dependencies declared once.** A task lists what it needs in `deps`, and those tasks run in parallel before it.
- **Starting points for common setups.** A multi-stage build, a Docker workflow, and a monorepo layout.
- **Taskfiles other people can use.** A `desc` on every task so `task --list` is useful, a `default` task, namespaced names such as `docker:build`, and includes to split large files.
- **Fast answers when something breaks.** Fixes for task not found, variables not expanding, dependencies not running, and file watching not working.
- **Advice on when not to use it.** If you need real programming-language features or complex conditional logic, the skill says so and points you to a script or a build system.

## How to use it

The skill loads on its own when you create, edit, or debug a Taskfile, or ask about tasks, dependencies, variables, includes, watching, or moving from Make:

```text
Convert this Makefile to a Taskfile and only rebuild when the Go sources change.
```

```text
Why isn't {{VERSION}} expanding in my build task?
```

## Install

See the [Quickstart](../../README.md#quickstart) in the main README.
