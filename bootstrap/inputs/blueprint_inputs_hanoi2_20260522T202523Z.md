# Blueprint Inputs: hanoi2

## Metadata
- Collected at (UTC): 2026-05-22T20:25:23+00:00

## Required Inputs
- projectSlug: hanoi2
- baseBranch: main
- existingRootDoc: AGENTS.md
- workflowsWanted: document, review, changelog

## Tech Stack
- Python3

## Constraints
### Core Rules
- Root doc remains minimal and links to canonical skill/workflow files
- Workflow IDs and file paths stay consistent across references
- Each workflow contract includes Goal, Scope, Triggers, Inputs, Invariants, Procedure, Outputs, Review gate, References
- Avoid duplication; link to the source of truth
- Scaffold only requested workflows
- All contract links resolve

### Stack-Specific Rules
- Use TDD for any task.
- Run ruff check and ensure coverage is 100% before suggesting commit.
- Write Pythonic code.
- Avoid regressions.
- Always use .venv.
- Always use Material Design for UI.
- "Clean the house" means checking for legacy or useless code.
- Always let the user test and review before suggesting a commit.

### Canonical Constraints
- Root doc remains minimal and links to canonical skill/workflow files
- Workflow IDs and file paths stay consistent across references
- Each workflow contract includes Goal, Scope, Triggers, Inputs, Invariants, Procedure, Outputs, Review gate, References
- Avoid duplication; link to the source of truth
- Scaffold only requested workflows
- All contract links resolve
- Use TDD for any task.
- Run ruff check and ensure coverage is 100% before suggesting commit.
- Write Pythonic code.
- Avoid regressions.
- Always use .venv.
- Always use Material Design for UI.
- "Clean the house" means checking for legacy or useless code.
- Always let the user test and review before suggesting a commit.

## Notes
- (none)

## Next Actions
1. Create/open your target project repository directory and switch to it.
2. Create `bootstrap/inputs/` in the target repo and move the generated input JSON/Markdown snapshots there.
3. Keep `blue_print_used_on_creation.md` at the target repository root.
4. Copy selected workflow folders from official AWB: document, review, changelog.
5. Copy related runbooks from official AWB: document-review-changelog.md.
6. Copy `AGENTS.md` from official AWB as a starting point, then adapt it for the target project.
7. Run your normal project setup/validation in the target repo and begin implementation there only.
