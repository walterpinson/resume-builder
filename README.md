# resume-builder

A local, file-based tool for generating tailored resumes and cover letters from a structured database of your professional experience. Drop in a job requisition; get a bespoke resume and cover letter as PDF.

No servers. No cloud. Everything runs on your machine.

---

## Prerequisites

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/) — Python package and environment manager

Install uv if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Installation

```bash
git clone https://github.com/yourhandle/resume-builder.git
cd resume-builder
uv sync
```

---

## Configuration

Copy the example config and fill in your details:

```bash
cp config.toml.example config.toml
```

Open `config.toml` and update the `[contact]` section. This file is gitignored and will never be committed.

```toml
[contact]
name     = "Your Name"
email    = "you@example.com"
phone    = "555-000-0000"
location = "City, ST"
linkedin = "yourhandle"
github   = "yourhandle"
website  = ""
```

---

## Running commands

All commands are run through the `rb` entry point via `uv run`:

```bash
uv run rb <command> [subcommand] [options]
```

Run `uv run rb --help` at any time to see available commands.

---

## CLI Reference

### `rb init`

Initialize (or re-initialize) the database schema. Run this once after setup.

```bash
uv run rb init
```

---

### Companies — `rb company`

| Command | Description |
|---|---|
| `rb company list` | List all companies |
| `rb company add` | Add a company (interactive prompts) |
| `rb company edit <id>` | Edit a company by ID |
| `rb company delete <id>` | Delete a company and all linked roles |

---

### Roles — `rb role`

Each role belongs to a company. Use `rb company list` to find company IDs.

| Command | Description |
|---|---|
| `rb role list` | List all roles |
| `rb role list --company <id>` | List roles for a specific company |
| `rb role show <id>` | Show full detail for a role, including accomplishments |
| `rb role add` | Add a role (interactive prompts) |
| `rb role edit <id>` | Edit a role by ID |
| `rb role delete <id>` | Delete a role and all its accomplishments |

---

### Accomplishments — `rb acc`

Accomplishments are the atomic unit for resume generation. Each is linked to a role.

| Command | Description |
|---|---|
| `rb acc list <role_id>` | List accomplishments for a role |
| `rb acc add` | Add an accomplishment (interactive prompts) |
| `rb acc edit <id>` | Edit an accomplishment by ID |
| `rb acc delete <id>` | Delete an accomplishment by ID |

**Fields:**
- `description` — one-sentence action + impact statement
- `metric` — quantified result (e.g. "300% revenue increase", "$2M cost savings")
- `impact_area` — `leadership` | `technical` | `business` | `product` | `cross-functional`
- `tags` — comma-separated keywords used during generation matching
- `weight` — 1–5; controls how prominently this accomplishment is featured (5 = always include)

---

### Skills — `rb skill`

| Command | Description |
|---|---|
| `rb skill list` | List all skills |
| `rb skill list --category <cat>` | Filter by category |
| `rb skill add` | Add a skill (interactive prompts) |
| `rb skill edit <id>` | Edit a skill by ID |
| `rb skill delete <id>` | Delete a skill by ID |
| `rb skill link <role_id> <skill_id>` | Associate a skill with a role |

**Categories:** `language` | `framework` | `cloud` | `methodology` | `tool` | `domain` | `platform`

**Proficiency levels:** `expert` | `proficient` | `familiar`

---

### Education — `rb edu`

| Command | Description |
|---|---|
| `rb edu list` | List all education entries |
| `rb edu add` | Add an education entry (interactive prompts) |
| `rb edu delete <id>` | Delete an education entry |

---

### Certifications — `rb cert`

| Command | Description |
|---|---|
| `rb cert list` | List all certifications |
| `rb cert add` | Add a certification (interactive prompts) |
| `rb cert delete <id>` | Delete a certification |

---

### Awards — `rb awards` / `rb award-add`

| Command | Description |
|---|---|
| `rb awards` | List all awards and recognition |
| `rb award-add` | Add an award (interactive prompts) |

---

### Patents — `rb patents` / `rb patent-add`

| Command | Description |
|---|---|
| `rb patents` | List all patents |
| `rb patent-add` | Add a patent (interactive prompts) |

---

### Security Clearances — `rb clearances` / `rb clearance-add`

| Command | Description |
|---|---|
| `rb clearances` | List all security clearances |
| `rb clearance-add` | Add a clearance (interactive prompts) |

---

### Raw Notes — `rb note`

A catch-all for career material that doesn't fit a structured table.

| Command | Description |
|---|---|
| `rb note list` | List all notes |
| `rb note add` | Add a note (opens editor if no body provided) |
| `rb note delete <id>` | Delete a note |

---

## Project structure

```
resume-builder/
├── config.toml.example     # committed — copy to config.toml and fill in
├── config.toml             # gitignored — your local contact details
├── pyproject.toml          # dependencies and entry point definition
├── src/resume_builder/     # application source
│   ├── config.py           # config loader and path resolution
│   ├── models.py           # dataclasses mirroring DB tables
│   ├── db/
│   │   ├── schema.sql      # database schema (source of truth)
│   │   └── ops.py          # all database read/write operations
│   ├── ingest/
│   │   └── pdf.py          # PDF text extraction for ingestion
│   └── cli/
│       └── commands.py     # Click CLI entry point
├── db/                     # gitignored — contains resume.db
└── output/                 # gitignored — generated PDFs land here
```

---

## Data that is never committed

The following are all gitignored:

| Path | Contents |
|---|---|
| `config.toml` | Your name, email, phone, location |
| `db/` | The SQLite database (your entire career history) |
| `data/` | Source PDFs used for ingestion |
| `output/` | Generated resumes and cover letters |
