"""All database read/write operations."""
import sqlite3
from typing import Optional

from resume_builder.db import connect


# ---------------------------------------------------------------------------
# Companies
# ---------------------------------------------------------------------------

def list_companies() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM companies ORDER BY name").fetchall()


def get_company(company_id: int) -> Optional[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM companies WHERE id=?", (company_id,)).fetchone()


def add_company(name: str, industry: str = None, website: str = None) -> int:
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO companies (name, industry, website) VALUES (?,?,?)",
            (name, industry, website),
        )
        conn.commit()
        return cur.lastrowid


def update_company(company_id: int, **kwargs) -> None:
    allowed = {"name", "industry", "website"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    sets = ", ".join(f"{k}=?" for k in fields)
    with connect() as conn:
        conn.execute(f"UPDATE companies SET {sets} WHERE id=?", (*fields.values(), company_id))
        conn.commit()


def delete_company(company_id: int) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM companies WHERE id=?", (company_id,))
        conn.commit()


# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------

def list_roles(company_id: int = None) -> list[sqlite3.Row]:
    with connect() as conn:
        if company_id:
            return conn.execute(
                "SELECT r.*, c.name as company_name FROM roles r "
                "JOIN companies c ON c.id=r.company_id "
                "WHERE r.company_id=? ORDER BY r.start_date DESC",
                (company_id,),
            ).fetchall()
        return conn.execute(
            "SELECT r.*, c.name as company_name FROM roles r "
            "JOIN companies c ON c.id=r.company_id "
            "ORDER BY r.start_date DESC"
        ).fetchall()


def get_role(role_id: int) -> Optional[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(
            "SELECT r.*, c.name as company_name FROM roles r "
            "JOIN companies c ON c.id=r.company_id WHERE r.id=?",
            (role_id,),
        ).fetchone()


def add_role(company_id: int, title: str, **kwargs) -> int:
    allowed = {"employment_type", "start_date", "end_date", "location", "location_type", "summary"}
    fields = {"company_id": company_id, "title": title}
    fields.update({k: v for k, v in kwargs.items() if k in allowed})
    cols = ", ".join(fields)
    placeholders = ", ".join("?" * len(fields))
    with connect() as conn:
        cur = conn.execute(f"INSERT INTO roles ({cols}) VALUES ({placeholders})", tuple(fields.values()))
        conn.commit()
        return cur.lastrowid


def update_role(role_id: int, **kwargs) -> None:
    allowed = {"company_id", "title", "employment_type", "start_date", "end_date",
               "location", "location_type", "summary"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    sets = ", ".join(f"{k}=?" for k in fields)
    with connect() as conn:
        conn.execute(f"UPDATE roles SET {sets} WHERE id=?", (*fields.values(), role_id))
        conn.commit()


def delete_role(role_id: int) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM roles WHERE id=?", (role_id,))
        conn.commit()


# ---------------------------------------------------------------------------
# Accomplishments
# ---------------------------------------------------------------------------

def list_accomplishments(role_id: int) -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM accomplishments WHERE role_id=? ORDER BY weight DESC, id",
            (role_id,),
        ).fetchall()


def get_accomplishment(acc_id: int) -> Optional[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM accomplishments WHERE id=?", (acc_id,)).fetchone()


def add_accomplishment(role_id: int, description: str, **kwargs) -> int:
    allowed = {"metric", "impact_area", "tags", "weight"}
    fields = {"role_id": role_id, "description": description}
    fields.update({k: v for k, v in kwargs.items() if k in allowed})
    cols = ", ".join(fields)
    placeholders = ", ".join("?" * len(fields))
    with connect() as conn:
        cur = conn.execute(
            f"INSERT INTO accomplishments ({cols}) VALUES ({placeholders})",
            tuple(fields.values()),
        )
        conn.commit()
        return cur.lastrowid


def update_accomplishment(acc_id: int, **kwargs) -> None:
    allowed = {"description", "metric", "impact_area", "tags", "weight"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    sets = ", ".join(f"{k}=?" for k in fields)
    with connect() as conn:
        conn.execute(f"UPDATE accomplishments SET {sets} WHERE id=?", (*fields.values(), acc_id))
        conn.commit()


def delete_accomplishment(acc_id: int) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM accomplishments WHERE id=?", (acc_id,))
        conn.commit()


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

def list_skills(category: str = None) -> list[sqlite3.Row]:
    with connect() as conn:
        if category:
            return conn.execute(
                "SELECT * FROM skills WHERE category=? ORDER BY name", (category,)
            ).fetchall()
        return conn.execute("SELECT * FROM skills ORDER BY category, name").fetchall()


def get_skill(skill_id: int) -> Optional[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM skills WHERE id=?", (skill_id,)).fetchone()


def add_skill(name: str, **kwargs) -> int:
    allowed = {"category", "proficiency", "last_used_year", "years_experience"}
    fields = {"name": name}
    fields.update({k: v for k, v in kwargs.items() if k in allowed})
    cols = ", ".join(fields)
    placeholders = ", ".join("?" * len(fields))
    with connect() as conn:
        cur = conn.execute(f"INSERT INTO skills ({cols}) VALUES ({placeholders})", tuple(fields.values()))
        conn.commit()
        return cur.lastrowid


def update_skill(skill_id: int, **kwargs) -> None:
    allowed = {"name", "category", "proficiency", "last_used_year", "years_experience"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    sets = ", ".join(f"{k}=?" for k in fields)
    with connect() as conn:
        conn.execute(f"UPDATE skills SET {sets} WHERE id=?", (*fields.values(), skill_id))
        conn.commit()


def delete_skill(skill_id: int) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM skills WHERE id=?", (skill_id,))
        conn.commit()


def link_skill_to_role(role_id: int, skill_id: int) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO role_skills (role_id, skill_id) VALUES (?,?)",
            (role_id, skill_id),
        )
        conn.commit()


# ---------------------------------------------------------------------------
# Education
# ---------------------------------------------------------------------------

def list_education() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM education ORDER BY year_completed DESC").fetchall()


def add_education(institution: str, degree: str, **kwargs) -> int:
    allowed = {"field", "focus", "year_completed"}
    fields = {"institution": institution, "degree": degree}
    fields.update({k: v for k, v in kwargs.items() if k in allowed})
    cols = ", ".join(fields)
    placeholders = ", ".join("?" * len(fields))
    with connect() as conn:
        cur = conn.execute(f"INSERT INTO education ({cols}) VALUES ({placeholders})", tuple(fields.values()))
        conn.commit()
        return cur.lastrowid


def update_education(edu_id: int, **kwargs) -> None:
    allowed = {"institution", "degree", "field", "focus", "year_completed"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    sets = ", ".join(f"{k}=?" for k in fields)
    with connect() as conn:
        conn.execute(f"UPDATE education SET {sets} WHERE id=?", (*fields.values(), edu_id))
        conn.commit()


def delete_education(edu_id: int) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM education WHERE id=?", (edu_id,))
        conn.commit()


# ---------------------------------------------------------------------------
# Certifications
# ---------------------------------------------------------------------------

def list_certifications() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM certifications ORDER BY year_issued DESC").fetchall()


def add_certification(name: str, **kwargs) -> int:
    allowed = {"issuing_org", "year_issued", "year_expires"}
    fields = {"name": name}
    fields.update({k: v for k, v in kwargs.items() if k in allowed})
    cols = ", ".join(fields)
    placeholders = ", ".join("?" * len(fields))
    with connect() as conn:
        cur = conn.execute(f"INSERT INTO certifications ({cols}) VALUES ({placeholders})", tuple(fields.values()))
        conn.commit()
        return cur.lastrowid


def update_certification(cert_id: int, **kwargs) -> None:
    allowed = {"name", "issuing_org", "year_issued", "year_expires"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    sets = ", ".join(f"{k}=?" for k in fields)
    with connect() as conn:
        conn.execute(f"UPDATE certifications SET {sets} WHERE id=?", (*fields.values(), cert_id))
        conn.commit()


def delete_certification(cert_id: int) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM certifications WHERE id=?", (cert_id,))
        conn.commit()


# ---------------------------------------------------------------------------
# Awards, Patents, Security Clearances, Raw Notes
# ---------------------------------------------------------------------------

def list_awards() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM awards ORDER BY year DESC").fetchall()


def add_award(name: str, **kwargs) -> int:
    allowed = {"role_id", "issuing_org", "year", "description"}
    fields = {"name": name}
    fields.update({k: v for k, v in kwargs.items() if k in allowed})
    cols = ", ".join(fields)
    placeholders = ", ".join("?" * len(fields))
    with connect() as conn:
        cur = conn.execute(f"INSERT INTO awards ({cols}) VALUES ({placeholders})", tuple(fields.values()))
        conn.commit()
        return cur.lastrowid


def list_patents() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM patents ORDER BY filing_date DESC").fetchall()


def add_patent(title: str, **kwargs) -> int:
    allowed = {"patent_number", "filing_date", "description"}
    fields = {"title": title}
    fields.update({k: v for k, v in kwargs.items() if k in allowed})
    cols = ", ".join(fields)
    placeholders = ", ".join("?" * len(fields))
    with connect() as conn:
        cur = conn.execute(f"INSERT INTO patents ({cols}) VALUES ({placeholders})", tuple(fields.values()))
        conn.commit()
        return cur.lastrowid


def list_clearances() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM security_clearances ORDER BY start_year DESC").fetchall()


def add_clearance(level: str, **kwargs) -> int:
    allowed = {"start_year", "end_year"}
    fields = {"level": level}
    fields.update({k: v for k, v in kwargs.items() if k in allowed})
    cols = ", ".join(fields)
    placeholders = ", ".join("?" * len(fields))
    with connect() as conn:
        cur = conn.execute(
            f"INSERT INTO security_clearances ({cols}) VALUES ({placeholders})",
            tuple(fields.values()),
        )
        conn.commit()
        return cur.lastrowid


def list_raw_notes() -> list[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM raw_notes ORDER BY created_at DESC").fetchall()


def add_raw_note(body: str, title: str = None, tags: str = None) -> int:
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO raw_notes (title, body, tags) VALUES (?,?,?)",
            (title, body, tags),
        )
        conn.commit()
        return cur.lastrowid


def delete_raw_note(note_id: int) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM raw_notes WHERE id=?", (note_id,))
        conn.commit()
