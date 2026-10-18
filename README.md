# Cybersecurity Tool Template

A reusable starting point for Python-based security tools — scanners, parsers,
recon utilities, automation scripts, whatever you're building next. Rename
`src/toolkit/` to your tool's actual name when you start a new project.

## Structure

```
.
├── src/toolkit/          # Your actual code lives here (rename "toolkit")
│   ├── cli.py             # Entry point / argument parsing
│   ├── core/               # Core logic modules (scanner.py, parser.py, etc.)
│   └── utils/               # Shared helpers (logging, config loading, I/O)
├── tests/                 # pytest test suite, mirrors src/ layout
├── config/                # YAML/JSON config files, kept out of code
├── logs/                  # Runtime logs (gitignored, .gitkeep only)
├── data/                  # Input/output data, wordlists, captures (gitignored)
├── docs/                  # Usage notes, write-ups for your portfolio
├── .github/workflows/     # CI: ruff + mypy + pytest on every push
├── .env.example             # Template for secrets/config — copy to .env
├── pyproject.toml           # Dependencies, console script, ruff/pytest/mypy config
└── Makefile                  # Shortcuts: make setup / test / lint / format / check
```

## Quickstart

```bash
git clone <your-new-repo-url>
cd <your-new-repo>
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
make setup                       # pip install -e ".[dev]" (tool + dev tooling)
cp .env.example .env             # fill in any secrets/config
make check                       # ruff + mypy + pytest, same as CI
toolkit --help                   # console script defined in pyproject.toml
```

## Why this layout

- **`src/` layout** keeps your package importable and testable without path
  hacks, and prevents accidentally running against uninstalled local files.
- **Separating `core/` from `cli.py`** means your actual logic is reusable
  and unit-testable independent of argument parsing — useful once a tool
  grows past a single script, and it demonstrates clean design in a
  portfolio review.
- **`config/` + `.env`** keeps secrets and environment-specific values out
  of git and out of your code.
- **CI from day one** means every tool you spin off this template already
  has lint + test checks running on GitHub — good practice to point to when
  talking about this work in interviews.

## Renaming for a new tool

1. `mv src/toolkit src/<your_tool_name>`
2. Update the import in `src/<your_tool_name>/cli.py` if needed
3. Update `pyproject.toml`: `[project] name`, `[project.scripts]`, and
   `--cov=` in `[tool.pytest.ini_options]`
4. Update this README's title and structure section
