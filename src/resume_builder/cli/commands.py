import click
from rich.console import Console
from rich.table import Table
from rich import box

from resume_builder.db import init_db
from resume_builder.db import ops

console = Console()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _table(*cols: str) -> Table:
    t = Table(box=box.SIMPLE_HEAD, show_lines=False)
    for col in cols:
        t.add_column(col)
    return t


def _confirm_delete(label: str) -> bool:
    return click.confirm(f"Delete {label}?", default=False)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------

@click.group()
def cli():
    """Resume Builder — manage your career database."""
    init_db()


# ---------------------------------------------------------------------------
# db init
# ---------------------------------------------------------------------------

@cli.command("init")
def cmd_init():
    """Initialize (or re-initialize) the database schema."""
    init_db()
    console.print("[green]Database initialized.[/green]")


# ---------------------------------------------------------------------------
# company
# ---------------------------------------------------------------------------

@cli.group("company")
def company():
    """Manage companies."""


@company.command("list")
def company_list():
    rows = ops.list_companies()
    t = _table("ID", "Name", "Industry", "Website")
    for r in rows:
        t.add_row(str(r["id"]), r["name"], r["industry"] or "", r["website"] or "")
    console.print(t)


@company.command("add")
@click.option("--name", prompt=True)
@click.option("--industry", default="", prompt="Industry (optional)")
@click.option("--website", default="", prompt="Website (optional)")
def company_add(name, industry, website):
    cid = ops.add_company(name, industry or None, website or None)
    console.print(f"[green]Added company #{cid}:[/green] {name}")


@company.command("edit")
@click.argument("company_id", type=int)
def company_edit(company_id):
    row = ops.get_company(company_id)
    if not row:
        console.print(f"[red]Company #{company_id} not found.[/red]")
        return
    name = click.prompt("Name", default=row["name"])
    industry = click.prompt("Industry", default=row["industry"] or "")
    website = click.prompt("Website", default=row["website"] or "")
    ops.update_company(company_id, name=name, industry=industry or None, website=website or None)
    console.print(f"[green]Updated company #{company_id}.[/green]")


@company.command("delete")
@click.argument("company_id", type=int)
def company_delete(company_id):
    row = ops.get_company(company_id)
    if not row:
        console.print(f"[red]Company #{company_id} not found.[/red]")
        return
    if _confirm_delete(f"company '{row['name']}' and all linked roles/accomplishments"):
        ops.delete_company(company_id)
        console.print("[green]Deleted.[/green]")


# ---------------------------------------------------------------------------
# role
# ---------------------------------------------------------------------------

@cli.group("role")
def role():
    """Manage roles."""


@role.command("list")
@click.option("--company", "company_id", type=int, default=None)
def role_list(company_id):
    rows = ops.list_roles(company_id)
    t = _table("ID", "Company", "Title", "Type", "Start", "End", "Location")
    for r in rows:
        t.add_row(
            str(r["id"]), r["company_name"], r["title"],
            r["employment_type"] or "", r["start_date"],
            r["end_date"] or "present", r["location"] or "",
        )
    console.print(t)


@role.command("show")
@click.argument("role_id", type=int)
def role_show(role_id):
    r = ops.get_role(role_id)
    if not r:
        console.print(f"[red]Role #{role_id} not found.[/red]")
        return
    console.print(f"\n[bold]{r['title']}[/bold] @ {r['company_name']}")
    console.print(f"  {r['start_date']} — {r['end_date'] or 'present'} | {r['location'] or 'N/A'} | {r['employment_type'] or 'N/A'}")
    if r["summary"]:
        console.print(f"\n{r['summary']}\n")
    accs = ops.list_accomplishments(role_id)
    if accs:
        console.print("[bold]Accomplishments:[/bold]")
        for a in accs:
            metric = f" [{a['metric']}]" if a["metric"] else ""
            console.print(f"  #{a['id']} (w:{a['weight']}) {a['description']}{metric}")


@role.command("add")
@click.option("--company-id", type=int, prompt="Company ID (rb company list to see IDs)")
@click.option("--title", prompt=True)
@click.option("--type", "employment_type", prompt="Employment type (full-time/contract/fractional/advisory/founder)", default="full-time")
@click.option("--start", "start_date", prompt="Start date (YYYY-MM)")
@click.option("--end", "end_date", prompt="End date (YYYY-MM or leave blank for current)", default="")
@click.option("--location", prompt="Location (City, ST)", default="")
@click.option("--location-type", prompt="Location type (remote/hybrid/on-site)", default="")
@click.option("--summary", prompt="Summary paragraph (optional)", default="")
def role_add(company_id, title, employment_type, start_date, end_date, location, location_type, summary):
    rid = ops.add_role(
        company_id, title,
        employment_type=employment_type or None,
        start_date=start_date,
        end_date=end_date or None,
        location=location or None,
        location_type=location_type or None,
        summary=summary or None,
    )
    console.print(f"[green]Added role #{rid}:[/green] {title}")


@role.command("edit")
@click.argument("role_id", type=int)
def role_edit(role_id):
    r = ops.get_role(role_id)
    if not r:
        console.print(f"[red]Role #{role_id} not found.[/red]")
        return
    title = click.prompt("Title", default=r["title"])
    employment_type = click.prompt("Employment type", default=r["employment_type"] or "")
    start_date = click.prompt("Start date", default=r["start_date"])
    end_date = click.prompt("End date (blank = current)", default=r["end_date"] or "")
    location = click.prompt("Location", default=r["location"] or "")
    location_type = click.prompt("Location type", default=r["location_type"] or "")
    summary = click.prompt("Summary", default=r["summary"] or "")
    ops.update_role(
        role_id,
        title=title,
        employment_type=employment_type or None,
        start_date=start_date,
        end_date=end_date or None,
        location=location or None,
        location_type=location_type or None,
        summary=summary or None,
    )
    console.print(f"[green]Updated role #{role_id}.[/green]")


@role.command("delete")
@click.argument("role_id", type=int)
def role_delete(role_id):
    r = ops.get_role(role_id)
    if not r:
        console.print(f"[red]Role #{role_id} not found.[/red]")
        return
    if _confirm_delete(f"role '{r['title']}' and all its accomplishments"):
        ops.delete_role(role_id)
        console.print("[green]Deleted.[/green]")


# ---------------------------------------------------------------------------
# accomplishment
# ---------------------------------------------------------------------------

@cli.group("acc")
def acc():
    """Manage accomplishments."""


@acc.command("list")
@click.argument("role_id", type=int)
def acc_list(role_id):
    rows = ops.list_accomplishments(role_id)
    t = _table("ID", "Wt", "Impact", "Description", "Metric")
    for r in rows:
        t.add_row(
            str(r["id"]), str(r["weight"]), r["impact_area"] or "",
            r["description"][:80], r["metric"] or "",
        )
    console.print(t)


@acc.command("add")
@click.option("--role-id", type=int, prompt="Role ID (rb role list to see IDs)")
@click.option("--description", prompt="Description (action + impact)")
@click.option("--metric", prompt="Metric (optional, e.g. '300% revenue increase')", default="")
@click.option("--impact", "impact_area", prompt="Impact area (leadership/technical/business/product/cross-functional)", default="")
@click.option("--tags", prompt="Tags (comma-separated, optional)", default="")
@click.option("--weight", type=int, prompt="Weight 1-5 (5 = always include)", default=3)
def acc_add(role_id, description, metric, impact_area, tags, weight):
    aid = ops.add_accomplishment(
        role_id, description,
        metric=metric or None,
        impact_area=impact_area or None,
        tags=tags or None,
        weight=weight,
    )
    console.print(f"[green]Added accomplishment #{aid}.[/green]")


@acc.command("edit")
@click.argument("acc_id", type=int)
def acc_edit(acc_id):
    r = ops.get_accomplishment(acc_id)
    if not r:
        console.print(f"[red]Accomplishment #{acc_id} not found.[/red]")
        return
    description = click.prompt("Description", default=r["description"])
    metric = click.prompt("Metric", default=r["metric"] or "")
    impact_area = click.prompt("Impact area", default=r["impact_area"] or "")
    tags = click.prompt("Tags", default=r["tags"] or "")
    weight = click.prompt("Weight 1-5", default=str(r["weight"]))
    ops.update_accomplishment(
        acc_id,
        description=description,
        metric=metric or None,
        impact_area=impact_area or None,
        tags=tags or None,
        weight=int(weight),
    )
    console.print(f"[green]Updated accomplishment #{acc_id}.[/green]")


@acc.command("delete")
@click.argument("acc_id", type=int)
def acc_delete(acc_id):
    r = ops.get_accomplishment(acc_id)
    if not r:
        console.print(f"[red]Accomplishment #{acc_id} not found.[/red]")
        return
    if _confirm_delete(f"accomplishment #{acc_id}"):
        ops.delete_accomplishment(acc_id)
        console.print("[green]Deleted.[/green]")


# ---------------------------------------------------------------------------
# skill
# ---------------------------------------------------------------------------

@cli.group("skill")
def skill():
    """Manage skills."""


@skill.command("list")
@click.option("--category", default=None)
def skill_list(category):
    rows = ops.list_skills(category)
    t = _table("ID", "Name", "Category", "Proficiency", "Last Used", "Years")
    for r in rows:
        t.add_row(
            str(r["id"]), r["name"], r["category"] or "", r["proficiency"] or "",
            str(r["last_used_year"] or ""), str(r["years_experience"] or ""),
        )
    console.print(t)


@skill.command("add")
@click.option("--name", prompt=True)
@click.option("--category", prompt="Category (language/framework/cloud/methodology/tool/domain/platform)", default="")
@click.option("--proficiency", prompt="Proficiency (expert/proficient/familiar)", default="proficient")
@click.option("--last-used", "last_used_year", type=int, prompt="Last used year", default=0)
@click.option("--years", "years_experience", type=int, prompt="Years experience", default=0)
def skill_add(name, category, proficiency, last_used_year, years_experience):
    sid = ops.add_skill(
        name,
        category=category or None,
        proficiency=proficiency or None,
        last_used_year=last_used_year or None,
        years_experience=years_experience or None,
    )
    console.print(f"[green]Added skill #{sid}:[/green] {name}")


@skill.command("edit")
@click.argument("skill_id", type=int)
def skill_edit(skill_id):
    r = ops.get_skill(skill_id)
    if not r:
        console.print(f"[red]Skill #{skill_id} not found.[/red]")
        return
    name = click.prompt("Name", default=r["name"])
    category = click.prompt("Category", default=r["category"] or "")
    proficiency = click.prompt("Proficiency", default=r["proficiency"] or "")
    last_used_year = click.prompt("Last used year", default=str(r["last_used_year"] or ""))
    years_experience = click.prompt("Years experience", default=str(r["years_experience"] or ""))
    ops.update_skill(
        skill_id,
        name=name,
        category=category or None,
        proficiency=proficiency or None,
        last_used_year=int(last_used_year) if last_used_year else None,
        years_experience=int(years_experience) if years_experience else None,
    )
    console.print(f"[green]Updated skill #{skill_id}.[/green]")


@skill.command("delete")
@click.argument("skill_id", type=int)
def skill_delete(skill_id):
    r = ops.get_skill(skill_id)
    if not r:
        console.print(f"[red]Skill #{skill_id} not found.[/red]")
        return
    if _confirm_delete(f"skill '{r['name']}'"):
        ops.delete_skill(skill_id)
        console.print("[green]Deleted.[/green]")


@skill.command("link")
@click.argument("role_id", type=int)
@click.argument("skill_id", type=int)
def skill_link(role_id, skill_id):
    ops.link_skill_to_role(role_id, skill_id)
    console.print(f"[green]Linked skill #{skill_id} to role #{role_id}.[/green]")


# ---------------------------------------------------------------------------
# education
# ---------------------------------------------------------------------------

@cli.group("edu")
def edu():
    """Manage education."""


@edu.command("list")
def edu_list():
    rows = ops.list_education()
    t = _table("ID", "Institution", "Degree", "Field", "Focus", "Year")
    for r in rows:
        t.add_row(
            str(r["id"]), r["institution"], r["degree"],
            r["field"] or "", r["focus"] or "", str(r["year_completed"] or ""),
        )
    console.print(t)


@edu.command("add")
@click.option("--institution", prompt=True)
@click.option("--degree", prompt=True)
@click.option("--field", prompt="Field of study (optional)", default="")
@click.option("--focus", prompt="Focus/concentration (optional)", default="")
@click.option("--year", "year_completed", type=int, prompt="Year completed", default=0)
def edu_add(institution, degree, field, focus, year_completed):
    eid = ops.add_education(
        institution, degree,
        field=field or None,
        focus=focus or None,
        year_completed=year_completed or None,
    )
    console.print(f"[green]Added education #{eid}.[/green]")


@edu.command("delete")
@click.argument("edu_id", type=int)
def edu_delete(edu_id):
    if _confirm_delete(f"education #{edu_id}"):
        ops.delete_education(edu_id)
        console.print("[green]Deleted.[/green]")


# ---------------------------------------------------------------------------
# certification
# ---------------------------------------------------------------------------

@cli.group("cert")
def cert():
    """Manage certifications."""


@cert.command("list")
def cert_list():
    rows = ops.list_certifications()
    t = _table("ID", "Name", "Org", "Issued", "Expires")
    for r in rows:
        t.add_row(
            str(r["id"]), r["name"], r["issuing_org"] or "",
            str(r["year_issued"] or ""), str(r["year_expires"] or ""),
        )
    console.print(t)


@cert.command("add")
@click.option("--name", prompt=True)
@click.option("--org", "issuing_org", prompt="Issuing org", default="")
@click.option("--year", "year_issued", type=int, prompt="Year issued", default=0)
@click.option("--expires", "year_expires", type=int, prompt="Year expires (0 = no expiry)", default=0)
def cert_add(name, issuing_org, year_issued, year_expires):
    cid = ops.add_certification(
        name,
        issuing_org=issuing_org or None,
        year_issued=year_issued or None,
        year_expires=year_expires or None,
    )
    console.print(f"[green]Added certification #{cid}.[/green]")


@cert.command("delete")
@click.argument("cert_id", type=int)
def cert_delete(cert_id):
    if _confirm_delete(f"certification #{cert_id}"):
        ops.delete_certification(cert_id)
        console.print("[green]Deleted.[/green]")


# ---------------------------------------------------------------------------
# Misc: awards, patents, clearances, notes
# ---------------------------------------------------------------------------

@cli.command("awards")
def awards_list():
    """List awards and recognition."""
    rows = ops.list_awards()
    t = _table("ID", "Year", "Award", "Org")
    for r in rows:
        t.add_row(str(r["id"]), str(r["year"] or ""), r["name"], r["issuing_org"] or "")
    console.print(t)


@cli.command("award-add")
@click.option("--name", prompt=True)
@click.option("--org", "issuing_org", prompt="Issuing org", default="")
@click.option("--year", type=int, prompt="Year", default=0)
@click.option("--description", prompt="Description (optional)", default="")
@click.option("--role-id", type=int, default=None)
def award_add(name, issuing_org, year, description, role_id):
    """Add an award or recognition."""
    aid = ops.add_award(
        name,
        issuing_org=issuing_org or None,
        year=year or None,
        description=description or None,
        role_id=role_id,
    )
    console.print(f"[green]Added award #{aid}.[/green]")


@cli.command("patents")
def patents_list():
    """List patents."""
    rows = ops.list_patents()
    t = _table("ID", "Title", "Number", "Filed")
    for r in rows:
        t.add_row(str(r["id"]), r["title"], r["patent_number"] or "", r["filing_date"] or "")
    console.print(t)


@cli.command("patent-add")
@click.option("--title", prompt=True)
@click.option("--number", "patent_number", prompt="Patent number", default="")
@click.option("--filed", "filing_date", prompt="Filing date (YYYY-MM-DD)", default="")
@click.option("--description", prompt="Description (optional)", default="")
def patent_add(title, patent_number, filing_date, description):
    """Add a patent."""
    pid = ops.add_patent(
        title,
        patent_number=patent_number or None,
        filing_date=filing_date or None,
        description=description or None,
    )
    console.print(f"[green]Added patent #{pid}.[/green]")


@cli.command("clearances")
def clearances_list():
    """List security clearances."""
    rows = ops.list_clearances()
    t = _table("ID", "Level", "From", "To")
    for r in rows:
        t.add_row(str(r["id"]), r["level"], str(r["start_year"] or ""), str(r["end_year"] or "active"))
    console.print(t)


@cli.command("clearance-add")
@click.option("--level", prompt="Clearance level (e.g. 'Top Secret/SCI')")
@click.option("--start", "start_year", type=int, prompt="Start year", default=0)
@click.option("--end", "end_year", type=int, prompt="End year (0 = active)", default=0)
def clearance_add(level, start_year, end_year):
    """Add a security clearance."""
    cid = ops.add_clearance(level, start_year=start_year or None, end_year=end_year or None)
    console.print(f"[green]Added clearance #{cid}.[/green]")


@cli.group("note")
def note():
    """Manage raw notes."""


@note.command("list")
def note_list():
    rows = ops.list_raw_notes()
    t = _table("ID", "Created", "Title", "Body (preview)")
    for r in rows:
        t.add_row(str(r["id"]), r["created_at"][:10], r["title"] or "", r["body"][:60])
    console.print(t)


@note.command("add")
@click.option("--title", prompt="Title (optional)", default="")
@click.option("--tags", prompt="Tags (optional)", default="")
@click.argument("body", required=False)
def note_add(title, tags, body):
    """Add a raw note. Pass body as argument or be prompted."""
    if not body:
        body = click.edit("") or ""
    if not body.strip():
        console.print("[yellow]Empty note — nothing saved.[/yellow]")
        return
    nid = ops.add_raw_note(body, title=title or None, tags=tags or None)
    console.print(f"[green]Added note #{nid}.[/green]")


@note.command("delete")
@click.argument("note_id", type=int)
def note_delete(note_id):
    if _confirm_delete(f"note #{note_id}"):
        ops.delete_raw_note(note_id)
        console.print("[green]Deleted.[/green]")
