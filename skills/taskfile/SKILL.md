---
name: taskfile
description: Expert guidance for Taskfile (taskfile.dev) — the YAML task runner. Use when creating, editing, debugging, or optimizing a Taskfile.yml, or when the user asks about tasks, task dependencies, variables, includes, file watching, or migrating from Make.
---

# Taskfile Expert

You are an expert in Taskfile (taskfile.dev), a modern task runner and build tool. Help users create, modify, and optimize Taskfiles for their projects.

## Core Principles

1. **Taskfile is a YAML-based task runner** - Similar to Makefile but designed for modern workflows
2. **Cross-platform by design** - Works consistently across Windows, macOS, and Linux
3. **Declarative syntax** - Clear, readable task definitions with minimal boilerplate
4. **Built-in features** - Variables, dependencies, file watching, and more without external plugins

## Basic Taskfile Structure

Always use version 3 (current stable):

```yaml
version: '3'

vars:
  # Global variables accessible to all tasks
  PROJECT_NAME: myapp
  BUILD_DIR: ./build

tasks:
  default:
    desc: Default task (runs when you type 'task' without arguments)
    cmds:
      - echo "Hello from Taskfile!"

  task-name:
    desc: Brief description of what this task does
    cmds:
      - command1
      - command2
```

## Key Features and Syntax

### Task Definition

```yaml
tasks:
  build:
    desc: Build the application
    summary: |
      Extended description that appears in help.
      Can span multiple lines.
    cmds:
      - go build -o {{.BUILD_DIR}}/app
    silent: false  # Set to true to suppress command echoing
```

### Variables

Variables can be defined at multiple levels with precedence order (highest to lowest):
1. Task-level variables
2. Command-line variables (`task VAR=value`)
3. Environment variables
4. Taskfile-level variables

```yaml
version: '3'

vars:
  # Static variables
  GREETING: Hello, World!

  # Dynamic variables (command output)
  GIT_COMMIT:
    sh: git rev-parse --short HEAD

  # Variables with defaults
  ENV: {sh: echo ${ENVIRONMENT:-development}}

tasks:
  greet:
    vars:
      # Task-specific variable
      NAME: Developer
    cmds:
      - echo "{{.GREETING}}, {{.NAME}}"
      - echo "Commit: {{.GIT_COMMIT}}"
```

### Dependencies

```yaml
tasks:
  # Dependencies run in parallel by default
  build:
    deps: [install, lint, test]
    cmds:
      - go build

  # Force sequential execution
  deploy:
    deps:
      - task: build
      - task: push
    cmds:
      - kubectl apply -f deployment.yaml

  install:
    cmds:
      - go mod download

  lint:
    cmds:
      - golangci-lint run

  test:
    cmds:
      - go test ./...
```

### Sources and Status (Smart Task Execution)

Run tasks only when files change:

```yaml
tasks:
  build:
    desc: Build only if source files changed
    sources:
      - src/**/*.go
      - go.mod
      - go.sum
    generates:
      - bin/app
    cmds:
      - go build -o bin/app

  # Alternative: use status for custom checks
  compile-assets:
    status:
      - test -f dist/bundle.js
      - test dist/bundle.js -nt src/index.js
    cmds:
      - npm run build
```

### Environment Variables

```yaml
version: '3'

env:
  # Global environment variables
  GO111MODULE: on
  CGO_ENABLED: "0"

dotenv:
  - .env          # Load from .env file
  - .env.local    # Override with local settings

tasks:
  test:
    env:
      # Task-specific environment
      TEST_DATABASE: postgres://localhost/test_db
    cmds:
      - go test ./...
```

### Platform-Specific Commands

```yaml
tasks:
  build:
    cmds:
      - echo "Building for {{OS}}/{{ARCH}}"

  install:
    platforms: [linux, darwin]  # Only run on Linux/macOS
    cmds:
      - brew install tool

  install-windows:
    platforms: [windows]
    cmds:
      - choco install tool
```

### Preconditions

```yaml
tasks:
  deploy:
    preconditions:
      - sh: git diff-index --quiet HEAD
        msg: "Working directory must be clean"
      - test -f .env.production
      - sh: kubectl cluster-info
        msg: "Cannot connect to cluster"
    cmds:
      - kubectl apply -f k8s/
```

### Including Other Taskfiles

```yaml
version: '3'

includes:
  docker: ./docker/Taskfile.yml
  k8s:
    taskfile: ./kubernetes/Taskfile.yml
    dir: ./kubernetes  # Run tasks in this directory

tasks:
  all:
    deps:
      - docker:build
      - k8s:deploy
```

### Interactive Commands

```yaml
tasks:
  shell:
    interactive: true
    cmds:
      - docker exec -it mycontainer /bin/bash
```

### Looping

```yaml
tasks:
  test-all:
    vars:
      MODULES:
        sh: ls -d */
    cmds:
      - for: { var: MODULES }
        cmd: go test ./{{.ITEM}}

  # Or with static list
  lint-files:
    vars:
      FILES: [main.go, utils.go, config.go]
    cmds:
      - for: { var: FILES }
        cmd: golangci-lint run {{.ITEM}}
```

### File Watching

```yaml
tasks:
  dev:
    desc: Watch for changes and rebuild
    watch: true
    sources:
      - "**/*.go"
    cmds:
      - go build
      - ./app
```

## Common Patterns

### Multi-Stage Build Process

```yaml
version: '3'

vars:
  APP_NAME: myapp
  BUILD_DIR: ./dist

tasks:
  default:
    deps: [build]

  clean:
    desc: Remove build artifacts
    cmds:
      - rm -rf {{.BUILD_DIR}}

  deps:
    desc: Install dependencies
    sources:
      - go.mod
      - go.sum
    cmds:
      - go mod download
    generates:
      - go.sum

  lint:
    desc: Run linters
    deps: [deps]
    cmds:
      - golangci-lint run

  test:
    desc: Run tests
    deps: [deps]
    cmds:
      - go test -v ./...

  build:
    desc: Build application
    deps: [deps, lint, test]
    sources:
      - "**/*.go"
      - go.mod
      - go.sum
    generates:
      - "{{.BUILD_DIR}}/{{.APP_NAME}}"
    cmds:
      - mkdir -p {{.BUILD_DIR}}
      - go build -o {{.BUILD_DIR}}/{{.APP_NAME}}
```

### Docker Workflow

```yaml
version: '3'

vars:
  IMAGE_NAME: myapp
  TAG:
    sh: git rev-parse --short HEAD

tasks:
  docker:build:
    desc: Build Docker image
    cmds:
      - docker build -t {{.IMAGE_NAME}}:{{.TAG}} .
      - docker tag {{.IMAGE_NAME}}:{{.TAG}} {{.IMAGE_NAME}}:latest

  docker:push:
    desc: Push image to registry
    deps: [docker:build]
    cmds:
      - docker push {{.IMAGE_NAME}}:{{.TAG}}
      - docker push {{.IMAGE_NAME}}:latest

  docker:run:
    desc: Run container locally
    deps: [docker:build]
    cmds:
      - docker run -p 8080:8080 {{.IMAGE_NAME}}:latest
```

### Monorepo Management

```yaml
version: '3'

includes:
  frontend:
    taskfile: ./apps/frontend/Taskfile.yml
    dir: ./apps/frontend
  backend:
    taskfile: ./apps/backend/Taskfile.yml
    dir: ./apps/backend
  shared:
    taskfile: ./packages/shared/Taskfile.yml
    dir: ./packages/shared

tasks:
  install:
    desc: Install all dependencies
    cmds:
      - task: frontend:install
      - task: backend:install
      - task: shared:install

  build:
    desc: Build all packages
    cmds:
      - task: shared:build
      - task: frontend:build
      - task: backend:build

  test:
    desc: Run all tests
    cmds:
      - task: shared:test
      - task: frontend:test
      - task: backend:test
```

## Best Practices

1. **Always specify version** - Use `version: '3'` at the top
2. **Add descriptions** - Use `desc:` for all tasks to make `task --list` useful
3. **Use variables for flexibility** - Define paths, names, and values as variables
4. **Leverage sources/generates** - Avoid unnecessary rebuilds
5. **Group related tasks** - Use colon notation (e.g., `docker:build`, `docker:push`)
6. **Set a default task** - Create a `default` task for common workflow
7. **Document complex tasks** - Use `summary:` for detailed explanations
8. **Use includes for organization** - Break large Taskfiles into smaller, focused ones
9. **Add preconditions** - Validate environment before running tasks
10. **Silent by default** - Use `silent: true` for cleaner output when appropriate

## Troubleshooting

### Common Issues

- **Task not found**: Check task name spelling and ensure you're in the correct directory
- **Variables not expanding**: Ensure proper `{{.VAR}}` syntax with dots
- **Dependencies not running**: Check task names in `deps:` array
- **File watching not working**: Ensure `sources:` paths are correct and `watch: true` is set

## Command Reference

```bash
# List all available tasks
task --list
task -l

# Run a task
task build

# Run multiple tasks
task clean build test

# Pass variables to tasks
task build VERSION=1.0.0

# Run task from specific Taskfile
task --taskfile ./path/to/Taskfile.yml build

# Watch for changes
task --watch dev

# Run task with increased verbosity
task --verbose build

# Show summary of a task
task --summary build
```

## When to Use Taskfile

**Good Use Cases:**
- Build automation and compilation
- Development workflows (lint, test, build)
- Docker and container management
- Deployment orchestration
- Database migrations
- Asset compilation
- CI/CD task definitions

**Consider Alternatives When:**
- You need programming language features (use a build tool native to your language)
- Complex conditional logic is required (consider a shell script or proper build system)
- You're working in a team that's heavily invested in another tool (e.g., Make, Just, etc.)

## Additional Resources

- Official Documentation: https://taskfile.dev
- GitHub Repository: https://github.com/go-task/task
- Installation: https://taskfile.dev/installation
