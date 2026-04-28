# Tech Stack & Dependencies

Reference document for understanding what's under the hood and why each piece was chosen.

---

## The `rb` command

`rb` is the CLI entry point for this tool. It's a short alias for "resume-builder," defined in `pyproject.toml`:

```toml
[project.scripts]
rb = "resume_builder.cli.commands:cli"
```

When you run `uv sync`, uv installs the package into a local virtual environment (`.venv/`) and registers `rb` as an executable script inside it. The `uv run` prefix ensures that script is found in that environment rather than your system PATH:

```bash
uv run rb company list
```

You can also activate the venv directly and drop `uv run` if you prefer:

```bash
source .venv/bin/activate
rb company list
```

---

## Runtime

### Python 3.11+
The minimum required version. Python 3.11 introduced `tomllib` into the standard library (used to parse `config.toml`), eliminating a dependency. Python 3.12 is what uv resolved to on this machine, which is fine.

---

## Package & Environment Management

### [uv](https://docs.astral.sh/uv/) — `astral-sh/uv`
Replaces pip + venv. Written in Rust; significantly faster than pip for dependency resolution and installation. Single command (`uv sync`) reads `pyproject.toml`, creates `.venv/`, and installs everything. The lockfile (`uv.lock`) pins exact versions so the environment is reproducible.

**Key commands:**
```bash
uv sync                  # install / update all dependencies
uv run rb <command>      # run a command in the managed environment
uv add <package>         # add a new dependency
uv remove <package>      # remove a dependency
```

---

## Build Backend

### [hatchling](https://hatch.pypa.io/latest/config/build/)
The build backend that packages this project. It handles the `src/` layout (source code lives in `src/resume_builder/` rather than the root) and wires up the `rb` entry point. Chosen because it's the modern, PEP 517-compliant default — no legacy `setup.py` baggage.

---

## Runtime Dependencies

### [click](https://click.palletsprojects.com/) `>=8.1`
The CLI framework. Handles argument parsing, command grouping, interactive prompts, and `--help` generation. It's the industry standard for Python CLIs — well-maintained by the Pallets project (same team as Flask). The entire `rb` command tree is built with Click decorators.

### [pdfplumber](https://github.com/jsvine/pdfplumber) `>=0.11`
PDF text extraction. Used during the ingestion step to pull text out of your seed resume and LinkedIn PDFs. Built on top of `pdfminer.six` and `pypdfium2`. Chosen over alternatives because it handles complex layouts (multi-column, tables) better than bare pdfminer and doesn't require external binaries like `pdftotext`.

**What it pulls in:**
- `pdfminer-six` — low-level PDF parsing
- `pypdfium2` — rendering engine (Google's PDFium, pre-compiled binary)
- `pillow` — image handling for PDFs with embedded images
- `cryptography` — handles encrypted/password-protected PDFs

### [rich](https://rich.readthedocs.io/) `>=13.0`
Terminal output formatting. Produces the styled tables you see when running `rb company list`, `rb role list`, etc. Also used for colored status messages (`[green]Added...[/green]`). Zero configuration required — it auto-detects terminal capabilities and degrades gracefully.

---

## Standard Library (no install required)

### `sqlite3`
The database engine. Ships with Python. The database is a single file at `db/resume.db` (gitignored). SQLite was chosen over JSON files because the career data has genuine relational structure — multiple roles per company, accomplishments per role, skills linked across roles — and SQLite handles that cleanly without hand-rolling joins.

### `tomllib`
Parses `config.toml`. Built into Python 3.11+, which is why that's the minimum version.

### `pathlib`
Path manipulation throughout the codebase. Preferred over `os.path` for its object-oriented API.

### `dataclasses`
Used in `models.py` to define typed representations of each database table. Not strictly required (the DB layer uses `sqlite3.Row` directly), but they serve as documentation of the schema in Python terms.

---

## Dependency Tree (as installed)

```
resume-builder
├── click 8.3.3
├── pdfplumber 0.11.9
│   ├── pdfminer-six 20251230
│   │   ├── charset-normalizer
│   │   └── cryptography
│   │       ├── cffi
│   │       └── pycparser
│   ├── pypdfium2 5.7.1
│   └── pillow 12.2.0
└── rich 15.0.0
    ├── markdown-it-py
    │   └── mdurl
    └── pygments
```

Total: 14 packages. No global installs; everything is contained in `.venv/`.

---

## What's intentionally absent

| Thing | Why excluded |
|---|---|
| ORM (SQLAlchemy, etc.) | Overhead not justified for a local single-user tool; raw `sqlite3` is sufficient and more transparent |
| Database migrations library (Alembic) | Schema is simple enough that `schema.sql` is run idempotently with `CREATE TABLE IF NOT EXISTS` |
| Testing framework | Not yet wired up — will add `pytest` under `[dependency-groups] dev` when Phase 5 is complete |
| Web framework | Explicitly out of scope per the brief — local-first, no servers |
| LLM SDK | Coming in Phase 5 (the generator); will be added then |
