# Blueprint Used on Creation

Official AWB source: `https://github.com/devton/agentic-workflow-blueprint`

## Required Preparation

- Before start, update `agentic-workflow-blueprint` repo.
- Run `make pre-bootstrap-audit` in this guide repository and proceed only if it passes.
- Review official blueprint files in `agentic-workflow-blueprint`.
- Open the target project repository in VS Code.
- Ask the LLM to review the current blueprint changes and this guidance repo.

## Initial Input Snapshot

- `projectSlug`: hanoi2
- `baseBranch`: main
- `existingRootDoc`: AGENTS.md
- `workflowsWanted`: document, review, changelog

### techStack
- Python3

### constraints (core rules)
- Root doc remains minimal and links to canonical skill/workflow files
- Workflow IDs and file paths stay consistent across references
- Each workflow contract includes Goal, Scope, Triggers, Inputs, Invariants, Procedure, Outputs, Review gate, References
- Avoid duplication; link to the source of truth
- Scaffold only requested workflows
- All contract links resolve

### constraints (stack-specific rules)
- Use TDD for any task.
- Run ruff check and ensure coverage is 100% before suggesting commit.
- Write Pythonic code.
- Avoid regressions.
- Always use .venv.
- Always use Material Design for UI.
- "Clean the house" means checking for legacy or useless code.
- Always let the user test and review before suggesting a commit.

### constraints (canonical)
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

## Boundary Rules

- Use official `agentic-workflow-blueprint` as source of truth for workflow structure and contracts.
- Execute scaffolding and implementation in the target project repository.
- Do not modify the official `agentic-workflow-blueprint` repository with project-specific implementation changes.
- Continue implementation from the new repository only after initial inputs are validated and initial artifacts are prepared.

## Migration Checklist to New Repo

- Create/open the target project repository directory.
- Move generated input snapshot files (`blueprint_inputs_*.json` and `blueprint_inputs_*.md`) into `bootstrap/inputs/` in the target repo.
- Keep this file as `blue_print_used_on_creation.md` at the target repo root.
- Copy files created during the initial inputs phase.
- Copy the required workflow files generated or selected from the blueprint flow.
- Copy selected official workflow folders: document, review, changelog.
- Copy runbook from official AWB: document-review-changelog.md.
- Copy `AGENTS.md` from official AWB as a starting point and adapt it for the target project.
- Ensure orchestration files are present in the new repo.
- Add project tooling files as needed by the chosen stack (post-handoff).
- Keep this file in the new repo root for traceability.

## Handoff Acknowledgement

- Initial inputs were reviewed and accepted.
- Initial artifacts were prepared.
- Project-specific implementation now continues only in the new repo.
- Official `agentic-workflow-blueprint` repository remains unchanged by project-specific work.
