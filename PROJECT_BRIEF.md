# Project: Bespoke Resume & Cover Letter Tooling

## Objective
Build a local, file-based system that generates tailored resumes and cover letters for specific job requisitions, grounded in a structured database of my professional experience. The end state: I drop in a job req, the tool produces a bespoke resume (1–3 pages) and cover letter as PDF.

## Build Philosophy
- **Local-first, no infrastructure.** No servers, no cloud DBs, no auth. Everything runs on my machine.
- **Iterative.** Build in phases. Each phase produces something usable before moving to the next.
- **Inspectable.** I should be able to open any data file and read it. Favor human-readable formats.
- **Stop and ask** when you hit a meaningful design decision rather than guessing. Show me options with tradeoffs.

## Phases

### Phase 1: Experience Database
- Propose a schema for storing my career data. Default to **SQLite** unless you see a strong reason to use JSON files; explain the choice briefly before committing.
- Schema must capture, at minimum: roles (company, title, dates, location), accomplishments (linked to roles, with metrics where available), skills (with proficiency and recency), education, certifications, projects, and a free-form "raw notes" table for things that don't fit cleanly.
- Build an ingestion step that reads my **old resume** and **LinkedIn export** (I'll provide both) and populates the database. Show me what you extracted before committing — I want to verify and correct.
- Provide simple CLI commands to view, add, edit, and delete entries.

### Phase 2: Interview Mode
- Build an interactive Q&A flow where you interview me about my **current role** specifically.
- The goal: capture the role in enough depth and with enough framing variety that it can be presented multiple ways depending on the target job.
- Ask about: scope, scale (people, budget, systems), measurable outcomes, technical contributions, leadership contributions, cross-functional work, and the "story" of what I changed or built.
- Store responses as structured accomplishments tied to the current role, plus a "framings" table that captures alternate ways to characterize the same work (e.g., "as an IC contribution" vs. "as a leadership outcome").
- This interview should be re-runnable — I'll want to add to it over time.

### Phase 3: Resume Format
- Develop a resume template that scales cleanly from **1 to 3 pages** based on a length parameter.
- HTML + CSS rendered to PDF is the default approach (use a library like WeasyPrint, Playwright, or wkhtmltopdf — pick one and justify briefly). Direct PDF generation is acceptable if you have a strong reason.
- Format should be ATS-friendly: standard fonts, no images of text, clean section headers, parseable structure.
- Visual design should be modern and confident but not gimmicky. Avoid the LaTeX-academic look and the over-designed-Canva look.
- Build a preview command so I can iterate on the design before wiring it to the generation logic.

### Phase 4: Cover Letter Format
- Companion template to the resume, same visual language.
- Should support a structured intro / body / close pattern with placeholders the generator fills in.

### Phase 5: The Generator (the payoff)
- Single command: I supply a job requisition (paste text, file path, or URL — support at least file path and pasted text).
- The tool:
  1. Parses the req for required skills, preferred skills, responsibilities, and seniority signals.
  2. Queries the experience database for the most relevant accomplishments and skills.
  3. Selects the appropriate framing of my current role.
  4. Drafts a tailored resume at the requested length (default: 2 pages).
  5. Drafts a tailored cover letter.
  6. Outputs both as PDF in an organized directory: `output/<company>_<role>_<date>/`.
- **Critical constraint: no fabrication.** Every claim in the resume must trace back to an entry in the experience database. If the req asks for something I don't have, omit it — do not invent. Make this a hard rule in the generation logic.
- Include a "rationale" file in each output directory explaining why specific accomplishments were chosen and which req requirements drove them. This is for my review and for tuning the system.

## Tech Stack Preferences
- Python is fine. Pick libraries that are well-maintained and unsurprising.
- Keep dependencies minimal.
- Use a `pyproject.toml` or equivalent. No global installs.

## What I Want From You Right Now
1. Acknowledge the brief and flag any ambiguities or decisions you want my input on before writing code.
2. Propose the project structure (directory layout, key files).
3. Propose the Phase 1 schema and wait for my approval before building.

Do not attempt to build all five phases in one shot. We go phase by phase, and I review at each gate.
