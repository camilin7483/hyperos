# Contributing to HyperOS

Thank you for your interest in contributing to HyperOS. This document outlines the process and standards for contributing.

## Code of Conduct

All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Development Standards

- Follow Clean Architecture principles
- Follow SOLID principles
- Prefer composition over inheritance
- Keep modules independent and loosely coupled
- Use descriptive naming for all symbols
- Avoid hardcoded paths — use configuration
- Avoid duplicated code — reuse through `core/`
- Every directory must contain documentation
- Every component should be designed for future expansion

## Language

All code, comments, documentation, commit messages, and identifiers must be written in **English**.

## Getting Started

1. Fork the repository
2. Set up the development environment:
   ```bash
   ./scripts/setup-dev.sh
   ```
3. Read the [ARCHITECTURE.md](ARCHITECTURE.md) and [BUILD.md](BUILD.md)
4. Check the [ROADMAP.md](ROADMAP.md) for current priorities

## Pull Request Process

1. Create a feature branch from `main`
2. Follow the code style of the existing codebase
3. Run linting before committing:
   ```bash
   ./scripts/lint.sh
   ```
4. Test your changes:
   ```bash
   ./scripts/test.sh
   ```
5. Update documentation if your change affects the public interface
6. Submit a pull request using the [template](.github/PULL_REQUEST_TEMPLATE/pull_request_template.md)

## Commit Messages

Follow conventional commits:

```
feat: add new feature
fix: correct a bug
docs: update documentation
refactor: restructure without changing behavior
perf: improve performance
chore: maintenance tasks
```

## Branch Naming

- `feat/<name>` — New features
- `fix/<name>` — Bug fixes
- `docs/<name>` — Documentation changes
- `refactor/<name>` — Code restructuring

## Questions

Open a discussion or issue if you have questions.
