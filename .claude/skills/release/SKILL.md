---
name: release
description: Manage releases for mcp-brasil — version bumping, changelog generation, git tagging, pushing, and PyPI publishing. Use this skill whenever the user says "release", "publish", "bump version", "new version", "lançar versão", "publicar", "criar release", or wants to prepare a package for distribution. Also trigger when the user asks about versioning, changelog, or PyPI publishing in this project.
argument-hint: -patch | -minor | -major [-dry] [-push] [-publish]
allowed-tools: Bash, Read, Grep, Glob
---

# Release

Manage the full release lifecycle: version bump, changelog, tag, push, and publish.

## Prerequisites

Before ANY release action, verify ALL of these (fail fast if any check fails):

1. **Clean working tree**: `git status --porcelain` must be empty
2. **On main branch**: `git rev-parse --abbrev-ref HEAD` must be `main`
3. **CI passes**: `make ci` must exit 0 (lint + types + tests)

If any check fails, tell the user what's wrong and stop. Do NOT proceed with a dirty tree or failing CI.

## Flags

| Flag | What it does |
|------|-------------|
| `-patch` | Bump patch version (0.1.0 → 0.1.1) |
| `-minor` | Bump minor version (0.1.0 → 0.2.0) |
| `-major` | Bump major version (0.1.0 → 1.0.0) |
| `-dry` | Show what would happen without executing |
| `-push` | After tagging, push commit + tag to remote |
| `-publish` | Push + build + publish to PyPI |
| (no flag) | Interactive — ask the user which bump type |

Flags can be combined: `/release -minor -publish` bumps minor, pushes, and publishes.

## Release Flow

### Step 1: Check prerequisites

```bash
# All three checks — stop on first failure
git status --porcelain          # must be empty
git rev-parse --abbrev-ref HEAD # must be "main"
make ci                         # must pass
```

### Step 2: Determine bump type

If no flag provided, show the current version and ask the user:

```bash
uv version   # shows current version
```

Then ask: "Which bump? patch / minor / major"

### Step 3: Bump version

```bash
uv version --bump <patch|minor|major>
```

Read back the new version: `uv version`

### Step 4: Generate changelog

If `git-cliff` is available:

```bash
git cliff --tag "v<NEW_VERSION>" -o CHANGELOG.md
```

If not available, skip and tell the user: "Install git-cliff for automatic changelog: `brew install git-cliff`"

### Step 5: Commit + Tag

```bash
git add pyproject.toml uv.lock CHANGELOG.md
git commit -m "chore(release): v<NEW_VERSION>"
git tag -a "v<NEW_VERSION>" -m "Release v<NEW_VERSION>"
```

### Step 6: Push (if -push or -publish)

```bash
git push origin main --follow-tags
```

### Step 7: Build + Publish (if -publish)

```bash
uv build
uv publish
```

If publishing fails due to missing token, tell the user:

```
Set your PyPI token:
  export UV_PUBLISH_TOKEN="pypi-AgEI..."

Or use trusted publishing (GitHub Actions):
  git push origin main --follow-tags
  # The release.yml workflow handles PyPI automatically
```

## Dry Run (-dry)

When `-dry` is specified, show the full plan without executing:

```
DRY RUN — Release Plan:

  Current version: 0.1.0
  New version:     0.2.0
  Bump type:       minor

  Steps:
  1. uv version --bump minor
  2. git cliff --tag "v0.2.0" -o CHANGELOG.md
  3. git add pyproject.toml uv.lock CHANGELOG.md
  4. git commit -m "chore(release): v0.2.0"
  5. git tag -a "v0.2.0" -m "Release v0.2.0"
  6. git push origin main --follow-tags    (if -push/-publish)
  7. uv build && uv publish               (if -publish)

  No changes made.
```

## Output

After a successful release, show a summary:

```
Release v0.2.0 complete!

  Version: 0.1.0 → 0.2.0
  Tag: v0.2.0
  Changelog: updated
  Pushed: yes/no
  Published: yes/no

  Next steps:
  - git push origin main --follow-tags    (if not pushed)
  - uv build && uv publish               (if not published)
  - Create GitHub release: gh release create v0.2.0 --generate-notes
```

## GitHub Release (bonus)

If the user asks to also create a GitHub release:

```bash
gh release create "v<NEW_VERSION>" --title "v<NEW_VERSION>" --generate-notes
```

Or with changelog-based notes:

```bash
git cliff --latest --strip header > /tmp/release-notes.md
gh release create "v<NEW_VERSION>" --title "v<NEW_VERSION>" --notes-file /tmp/release-notes.md
```

## Error Recovery

- **Dirty working tree**: Tell user to commit or stash first
- **Not on main**: Tell user to switch: `git checkout main`
- **CI fails**: Tell user to fix issues first, show the failing output
- **Push fails (no remote)**: Tell user to add remote: `git remote add origin <url>`
- **Publish fails (no token)**: Show token setup instructions
- **Tag already exists**: Tell user the version was already released
