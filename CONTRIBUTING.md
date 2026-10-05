# Contributing

This is a solo capstone project, but it follows standard GitHub workflow practices.

## Workflow

1. Create a branch for each feature or fix:
   git checkout -b feature/short-description

2. Make changes and commit with clear messages:
   git add .
   git commit -m "Add: brief description of change"

3. Push the branch:
   git push -u origin feature/short-description

4. Open a Pull Request on GitHub comparing the branch against main.

5. Review and merge -- merge into main once verified.

6. Delete the branch after merge:
   git branch -d feature/short-description

## Commit Message Conventions

- Add: new feature or file
- Fix: bug fix
- Update: modification to existing code
- Docs: documentation changes
- Refactor: code restructuring
- Test: adding or modifying tests

## Code Style

- Python 3.10+
- 4-space indentation
- Type hints on public functions
- Docstrings on modules and classes
