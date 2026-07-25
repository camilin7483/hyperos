# Contributing to HyperOS

Thank you for your interest in contributing to HyperOS. This document outlines everything you need to know to contribute effectively.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Development Standards](#development-standards)
3. [Architecture Overview](#architecture-overview)
4. [Getting Started](#getting-started)
5. [Creating a New Application](#creating-a-new-application)
6. [Adding a New Service to Core](#adding-a-new-service-to-core)
7. [Testing](#testing)
8. [Pull Request Process](#pull-request-process)
9. [Commit Guidelines](#commit-guidelines)
10. [Branch Naming](#branch-naming)
11. [Code Review](#code-review)
12. [Documentation](#documentation)
13. [Reporting Issues](#reporting-issues)

---

## Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming and inclusive environment for everyone.

---

## Development Standards

### Architecture

- **Clean Architecture** — Every application must follow the 4-layer Clean Architecture pattern:
  1. **Domain** — Pure Python data classes and enums (no framework dependencies)
  2. **Services** — Business logic (can use subprocess, system calls)
  3. **Widgets** — Reusable UI components (PySide6 only)
  4. **UI** — Application windows and pages (PySide6 only)

- **Dependency direction**: Domain ← Services ← Widgets ← UI (inward dependencies only)
- **No circular dependencies** between packages

### SOLID Principles

- **Single Responsibility** — Each class has one reason to change
- **Open/Closed** — Extend via inheritance or composition, don't modify
- **Liskov Substitution** — Derived classes must be substitutable for base
- **Interface Segregation** — Small, focused interfaces
- **Dependency Inversion** — Depend on abstractions, not concretions

### Code Style

- **Type hints** — Required for all function parameters and return values
- **Logging** — Use Python's `logging` module with `__name__` logger
- **Error handling** — Catch specific exceptions, never bare `except:`
- **Naming** — `snake_case` for functions/variables, `PascalCase` for classes
- **Line length** — Maximum 120 characters (prefer 100)
- **Comments** — English only, prefer self-documenting code

### Language Policy

All code, comments, documentation, commit messages, issue reports, and identifiers **must** be written in **English**.

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────┐
│                 GUI Applications                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │Welcome   │ │Center    │ │Settings  │ │Store   │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
├─────────────────────────────────────────────────────┤
│              Core Libraries (hyperos-core)           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │Services  │ │Widgets   │ │Domain    │ │UI Theme│ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
├─────────────────────────────────────────────────────┤
│           Configuration & System Services           │
│  systemd · udev · polkit · sysctl · config files    │
├─────────────────────────────────────────────────────┤
│               Arch Linux Base System                │
│  linux-zen · pacman · glibc · systemd · wayland     │
└─────────────────────────────────────────────────────┘
```

### Application Architecture (Clean Architecture)

```
hyper_<app>/
├── domain/
│   ├── __init__.py
│   └── models.py         # Pure data classes (no PySide6 dependency)
├── services/
│   ├── __init__.py
│   └── <name>_service.py  # Business logic, system interaction
├── widgets/
│   ├── __init__.py         # Reusable widgets (optional)
│   └── <widget>.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   └── <page>.py          # Page/section widgets
├── tests/
│   ├── __init__.py
│   └── test_<name>.py     # Unit tests
├── app.py                  # Entry point, QApplication setup
├── __init__.py
└── __main__.py
```

---

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/camilin7483/hyperos.git
cd hyperos
```

### 2. Set Up Development Environment

```bash
./scripts/setup-dev.sh
```

This installs required packages and sets up pre-commit hooks.

### 3. Read Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — System architecture overview
- [BUILD.md](BUILD.md) — Build instructions
- [ROADMAP.md](ROADMAP.md) — Current priorities

### 4. Find an Issue

Look for issues labeled:
- `good first issue` — For newcomers
- `help wanted` — Open for contribution
- `bug` — Bug fixes

### 5. Start Coding

```bash
# Create a feature branch
git checkout -b feat/my-feature

# Implement your changes
# ...

# Run tests
./scripts/test.sh

# Commit and push
git add .
git commit -m "feat: implement my feature"
git push origin feat/my-feature
```

---

## Creating a New Application

1. **Copy the template structure** from `packages/hyper-welcome/`
2. **Update metadata** in `pyproject.toml` and `PKGBUILD`
3. **Implement the domain layer** (`domain/models.py`, `domain/enums.py`)
4. **Implement service layer** (`services/`) — business logic
5. **Implement widgets** (`widgets/`) — reusable UI components
6. **Implement UI** (`ui/`) — windows and pages
7. **Implement entry point** (`app.py`)
8. **Write tests** (`tests/test_*.py`)
9. **Create desktop entry** (`data/hyper-<name>.desktop`)
10. **Create icon** (`assets/icons/hyper-<name>.svg`)
11. **Add to packages.x86_64** (`archiso/packages.x86_64`)

### Guidelines

- **Share code** through `hyperos-core` — don't duplicate services
- **Follow the pattern** of existing applications
- **Use dependency injection** for testability
- **Add logging** at INFO level for key operations
- **Handle errors** gracefully with fallbacks

---

## Adding a New Service to Core

1. Create the service in `core/hyperos_core/services/<name>.py`
2. Follow the existing pattern (type hints, logging, error handling)
3. Add domain models to `core/hyperos_core/domain/models.py` if needed
4. Write unit tests
5. Update the `core/__init__.py` exports if needed
6. Document usage in the service's docstring

---

## Testing

### Requirements

- **Every service** must have unit tests
- **Every application** must have integration tests
- **Critical paths** must have runtime validation tests

### Running Tests

```bash
# Run all tests
./scripts/test.sh

# Run tests for a specific app
cd packages/hyper-center/src
python -m pytest hyper_center/tests/ -v

# Run with coverage
python -m pytest --cov=hyper_center hyper_center/tests/
```

### Writing Tests

- Use `pytest` as the test runner
- Mock external calls (subprocess, file I/O, network) with `unittest.mock`
- Use fixtures for shared setup
- Test both success and failure paths
- Test edge cases (empty data, permission errors, timeouts)

```python
# Example test pattern
from unittest.mock import patch
from hyper_welcome.services.system_service import SystemService

class TestSystemService:
    def test_get_cpu_name(self):
        with patch("builtins.open", mock_open(read_data="model name : Intel CPU\n")):
            service = SystemService()
            result = service._get_cpu_name()
            assert "Intel" in result
```

---

## Pull Request Process

### 1. Prepare Your Changes

```bash
# Ensure your branch is up to date
git fetch origin
git rebase origin/main

# Run all checks
./scripts/lint.sh
./scripts/test.sh
```

### 2. Submit the PR

- Use the [pull request template](.github/PULL_REQUEST_TEMPLATE/pull_request_template.md)
- Clearly describe what your change does
- Link to any related issues
- List any breaking changes
- Include screenshots for UI changes

### 3. Review Process

1. **Automated checks** — CI must pass (lint, test, build)
2. **Code review** — At least one maintainer review
3. **Architecture review** — Changes to core/ or archiso/ require maintainer approval
4. **Documentation check** — Docs must be updated if interfaces change

### 4. Merge

- Squash commits into a single commit with a descriptive message
- Merge via `main` branch (no merge commits except for approved cases)

---

## Commit Guidelines

### Format

```
<type>: <short description>

<optional body>
<optional footer>
```

### Types

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding/modifying tests |
| `chore` | Maintenance (build, CI, deps) |
| `style` | Code style (formatting, naming) |

### Examples

```
feat: add CPU temperature monitoring to Hyper Center
fix: resolve NetworkService TypeError with default hosts
docs: update BUILD.md with QEMU UEFI instructions
refactor: extract shared service pattern to hyperos-core
test: add GPU detection tests for HardwareService
```

---

## Branch Naming

```
feat/<short-description>     # New features
fix/<short-description>      # Bug fixes
docs/<short-description>     # Documentation
refactor/<short-description> # Code restructuring
test/<short-description>     # Test additions
chore/<short-description>    # Maintenance
```

---

## Code Review

### What Reviewers Look For

- **Correctness** — Does the code work as intended?
- **Architecture** — Does it follow Clean Architecture?
- **Testing** — Are there adequate tests?
- **Error handling** — Are failures handled gracefully?
- **Style** — Does it follow the project style?
- **Performance** — Are there obvious performance issues?
- **Security** — Are there injection vectors or permission issues?

### Reviewer Etiquette

- Be constructive and specific
- Explain the "why" behind your feedback
- Approve when all major concerns are addressed
- Use GitHub's suggestion feature for minor fixes

---

## Documentation

### Required Documentation

- Every application must have a `README.md`
- Every package must have a `PKGBUILD` with a `pkgdesc`
- All public functions and classes must have docstrings
- Configuration files must have inline comments explaining each option

### Documentation Updates

Update documentation when:
- Adding a new feature
- Changing an existing interface
- Fixing a bug (add regression note to changelog)
- Updating configuration options

### CHANGELOG

Add entries to `CHANGELOG.md` under the appropriate version heading:

```markdown
## v0.5.0 — Next Release

### Added
- New feature description

### Changed
- Existing behavior description

### Fixed
- Bug fix description
```

---

## Reporting Issues

### Bug Reports

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md). Include:

- **Description** — What happened vs. what should happen
- **Steps to reproduce** — Exact steps to trigger the bug
- **Expected behavior** — What should have happened
- **Screenshots** — If applicable
- **Environment** — System info, HyperOS version
- **Logs** — Relevant log output

### Feature Requests

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md). Include:

- **Problem** — What problem does this solve?
- **Solution** — What should be implemented?
- **Alternatives** — What alternatives have been considered?
- **Priority** — How important is this for the next release?

---

## Getting Help

- **Issues** — Use GitHub issues for bug reports and feature requests
- **Discussions** — Use GitHub discussions for questions and ideas
- **Documentation** — Read `ARCHITECTURE.md`, `BUILD.md`, and `ROADMAP.md`

Thank you for contributing to HyperOS! 🚀
