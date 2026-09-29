---
name: create-pr
description: Group uncommitted changes into logical conventional commits, push them to a feature branch, and open a GitHub pull request with a release-please friendly description. Use when the user types /create-pr or asks to commit their changes and open a PR.
disable-model-invocation: true
---

# Create Pull Request with Release-Please Guidelines

This skill automates the process of committing changes, pushing to GitHub, and creating a Pull Request with a comprehensive description following Google release-please guidelines.

## Conventional Commit Types

- feat: New feature (triggers minor version bump)
- fix: Bug fix (triggers patch version bump)
- feat! or fix!: Breaking change (triggers major version bump)
- chore: Maintenance tasks (no version bump)
- docs: Documentation changes (no version bump)
- refactor: Code refactoring (no version bump)
- test: Test changes (no version bump)
- perf: Performance improvements (triggers patch version bump)

## Release-Please Guidelines

PR descriptions should include:

1. **Clear title**: Following conventional commits format
2. **Summary**: What changed and why
3. **Breaking Changes**: Clearly marked with BREAKING CHANGE: footer
4. **Related Issues**: Link to issues using Fixes or Closes keywords
5. **Test Plan**: How to verify the changes
6. **Release Notes**: User-facing description of changes

## Instructions for Claude

When this skill is invoked:

1. **Check git status and diff**:
   ```bash
   git status
   git diff --staged
   git diff
   ```

2. **Group changes into logical commits** by analyzing:
   - **By feature/functionality**: Group files that implement the same feature together
   - **By layer**: Keep related files together (e.g., API handler + its test file)
   - **By change type**: Separate refactoring from new features from bug fixes
   - **By scope**: Group changes affecting the same module/package

   Common grouping patterns:
   - `handler.go` + `handler_test.go` → one commit
   - `api.yaml` + generated `openapi/*.gen.go` → one commit
   - Multiple files for same feature → one commit
   - Unrelated fixes → separate commits
   - Test additions → can be separate or with implementation

3. **Determine commit type for each group**:
   - New features → feat
   - Bug fixes → fix
   - Breaking changes → Add ! suffix or BREAKING CHANGE: footer
   - Other changes → chore, refactor, docs, test, etc.

4. **Identify the scope for each commit** (optional but recommended):
   - Examples: `api`, `config`, `workflow`, `provider`, `auth`, etc.

5. **Check current branch**:
   ```bash
   git branch --show-current
   ```

6. **If on main/master, create a new feature branch**:
   ```bash
   git checkout -b <type>/<scope>-<short-description>
   ```
   Examples: `feat/api-appointment-slots`, `fix/auth-token-validation`

7. **Create commits for each logical group** (repeat for each group):
   ```bash
   # Stage only files for this commit group
   git add <file1> <file2> ...

   # Create the commit
   git commit -m "<type>(<scope>): <description>

   <body with detailed explanation>

   BREAKING CHANGE: <description if applicable>

   Fixes #<issue-number> (if applicable)"
   ```

   **Commit order**: Order commits so that reading them oldest-first explains the change,
   usually setup, then implementation, then tests and docs. Tests may share a commit with
   the code they cover.

8. **Push to remote**:
   ```bash
   git push -u origin <branch-name>
   ```

9. **Create PR with comprehensive description**:
   ```bash
   gh pr create --title "<primary-change-title>" --body "$(cat <<'EOF'
   ## Summary
   <1-3 sentence summary of what changed and why>

   ## Commits
   - `<short-sha>` <commit title>

   ## Changes
   - <bullet point list of key changes>
   - <each change should be clear and specific>

   ## Breaking Changes
   <If applicable, list breaking changes with migration guide>
   <If not applicable, write "None">

   ## Test Plan
   - [ ] <How to test the changes>
   - [ ] <Include specific curl commands or test steps>
   - [ ] <Verify no regressions>

   ## Related Issues
   Fixes #<issue-number> (if applicable)
   Closes #<issue-number> (if applicable)

   ## Release Notes
   <User-facing description for changelog>
   <Written from user perspective>
   <Highlight value and impact>

   ## Screenshots/Logs
   <If applicable, include relevant screenshots or log outputs>

   ## Checklist
   - [ ] Tests pass locally (project test command)
   - [ ] Linting passes (project lint command)
   - [ ] Documentation updated (if needed)
   - [ ] Breaking changes documented
   - [ ] Conventional commit format followed
   EOF
   )"
   ```

   **PR Title**: Use the primary/most significant change as the PR title. If all commits
   are of equal importance, use a summary title that encompasses the changes.

10. **Display PR URL** and confirm successful creation

## Important Notes

- **Create multiple logical commits** instead of one massive commit
- **Each commit should be atomic**: It should represent one logical change that could stand alone
- **Always follow Conventional Commits** format for commit messages
- **Use imperative mood** in commit descriptions (e.g., "add feature" not "added feature")
- **Keep commit title under 72 characters**
- **Breaking changes** must include BREAKING CHANGE: in commit footer or ! after type/scope
- **PR title** should reflect the primary change or summarize multiple changes
- **Verify all services** are properly tested before creating PR
- **Link related issues** using GitHub keywords (Fixes, Closes, Resolves)
- **Commit order should tell a story**: Reading commits chronologically should explain the progression of changes

## Example: Multiple Commits for a Feature

Given changes to implement appointment slot filtering, create separate commits:

**Commit 1 - API spec update:**
```
docs(api): add provider_type parameter to slots endpoint

Update OpenAPI spec with new query parameter for filtering
appointment slots by provider type.
```

**Commit 2 - Core implementation:**
```
feat(api): add appointment slot filtering by provider

Implement endpoint to filter available appointment slots based on
provider type and location preferences. This improves user experience
by showing only relevant appointment options.

- Add provider filter to slots endpoint
- Implement timezone conversion for slot times

Fixes #123
```

**Commit 3 - Tests:**
```
test(api): add tests for appointment slot filtering

Add unit tests covering filter logic, timezone conversion,
and edge cases for the new provider filtering feature.
```

## Example PR Description (Multiple Commits)

```markdown
## Summary
Adds appointment slot filtering by provider type to improve user experience when booking appointments.

## Commits
- `a1b2c3d` docs(api): add provider_type parameter to slots endpoint
- `e4f5g6h` feat(api): add appointment slot filtering by provider
- `i7j8k9l` test(api): add tests for appointment slot filtering

## Changes
- Added `provider_type` query parameter to `/v1/appointments/slots` endpoint
- Implemented timezone conversion for accurate slot display across regions
- Updated OpenAPI spec with new filtering parameters
- Added unit tests for filter logic and edge cases

## Breaking Changes
None

## Test Plan
- [ ] Run the test suite to verify all tests pass
- [ ] Test filtering with curl:
  ```bash
  curl -X GET "http://localhost:8080/v1/appointments/slots?start_date=2025-11-01&end_date=2025-11-15&provider_type=primary_care" \
    -H "Authorization: Bearer valid-jwt"
  ```
- [ ] Verify timezone handling for different user locations
- [ ] Test backward compatibility (endpoint works without filter)

## Related Issues
Fixes #123

## Release Notes
Users can now filter appointment slots by provider type, making it easier to find appointments with their preferred healthcare provider.

## Checklist
- [x] Tests pass locally (project test command)
- [x] Linting passes (project lint command)
- [x] Documentation updated
- [x] Conventional commit format followed
```

## When to Use Single vs Multiple Commits

**Use multiple commits when:**
- Changes span different concerns (API, tests, docs)
- Changes affect different modules/packages
- You have both bug fixes and new features
- Changes can be logically separated for easier review
- Implementation + tests can be split

**Use a single commit when:**
- All changes are tightly coupled and inseparable
- Very small change (few lines across 1-2 files)
- Single atomic change that makes no sense to split

## Usage

Invoke this skill with `/create-pr` and Claude will:
1. Analyze your uncommitted changes
2. Group changes into logical commit units
3. Create multiple commits in logical progression order
4. Push all commits to the feature branch
5. Generate a comprehensive PR with release-please compatible formatting
6. Open the PR on GitHub
