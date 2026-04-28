# CI Pipeline Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `.github/workflows/ci.yml` to include formatting checks and robust tool invocation.

**Architecture:** Modify the existing GitHub Actions workflow to use `python -m` for all tool calls and add a formatting check step.

**Tech Stack:** GitHub Actions, Python, Ruff, Bandit, Pytest

---

### Task 1: Update CI Workflow

**Files:**
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Update workflow file**

Replace the content of `.github/workflows/ci.yml` with the following:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'pip'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
        
    - name: Check formatting with Ruff
      run: |
        python -m ruff format --check .
        
    - name: Lint with Ruff
      run: |
        python -m ruff check .
        
    - name: Security scan with Bandit
      run: |
        python -m bandit -r src/
        
    - name: Test with pytest
      run: |
        python -m pytest --cov=src/tuleap_mcp --cov-report=xml tests/
```

- [ ] **Step 2: Verify formatting locally**

Run: `python -m ruff format --check .`
Expected: PASS (or fix formatting if it fails before committing)

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: enhance pipeline with formatting checks and robust tool calls"
```
