# Tower of Hanoi 2

![CI](https://github.com/zecafig/hanoi2/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/github/actions/workflow/status/zecafig/hanoi2/ci.yml?branch=main&label=coverage)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![pygame-ce](https://img.shields.io/badge/pygame--ce-2.x-00bcd4)
![Ruff](https://img.shields.io/badge/lint-ruff-46a758)
![Pytest](https://img.shields.io/badge/tests-pytest-0a9edc)

Tower of Hanoi game built with pygame-ce, developed as a second AI coding test in GitHub Copilot for VS Code.

## AI Test Metadata

- Tooling: GitHub Copilot (VS Code)
- LLM: GPT-5.3-Codex
- Test sequence: Second AI implementation test (follow-up to the first Hanoi project)

## Blueprint Provenance

This repository was constructed using the official blueprint flow and then implemented under those constraints.

- Official agentic-workflow-blueprint: https://github.com/devton/agentic-workflow-blueprint
- agentic-workflow-blueprint-guide used for this app bootstrap: [agentic_workflow_blueprint_guidance.md](agentic_workflow_blueprint_guidance.md)

## Project Summary

- Traditional Tower of Hanoi gameplay with 3 towers and variable piece count
- Piece count prompt before game starts
- Keyboard controls:
	- N: start a new game and enter a new piece count
	- A: autoplay optimal solution from a reset board
	- R: reset current game
	- Q: quit game
- Visual selection marker for currently selected tower
- Material-inspired visual palette

## Tech Stack

- Python
- pygame (via pygame-ce package)
- pytest
- pytest-cov
- ruff

## Local Run

```bash
source .venv/bin/activate
python -m pip install -e '.[dev]'
hanoi2
```

## Local Validation

```bash
source .venv/bin/activate
python -m ruff check .
python -m pytest --cov --cov-report=term-missing
```