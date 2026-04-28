PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL,
    industry  TEXT,
    website   TEXT
);

CREATE TABLE IF NOT EXISTS roles (
    id               INTEGER PRIMARY KEY,
    company_id       INTEGER REFERENCES companies(id),
    title            TEXT NOT NULL,
    employment_type  TEXT CHECK(employment_type IN ('full-time','contract','fractional','advisory','founder','part-time')),
    start_date       TEXT NOT NULL,
    end_date         TEXT,
    location         TEXT,
    location_type    TEXT CHECK(location_type IN ('remote','hybrid','on-site')),
    summary          TEXT
);

CREATE TABLE IF NOT EXISTS accomplishments (
    id           INTEGER PRIMARY KEY,
    role_id      INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    description  TEXT NOT NULL,
    metric       TEXT,
    impact_area  TEXT CHECK(impact_area IN ('leadership','technical','business','product','cross-functional')),
    tags         TEXT,
    weight       INTEGER NOT NULL DEFAULT 3 CHECK(weight BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS skills (
    id                INTEGER PRIMARY KEY,
    name              TEXT NOT NULL UNIQUE,
    category          TEXT CHECK(category IN ('language','framework','cloud','methodology','tool','domain','platform')),
    proficiency       TEXT CHECK(proficiency IN ('expert','proficient','familiar')),
    last_used_year    INTEGER,
    years_experience  INTEGER
);

CREATE TABLE IF NOT EXISTS role_skills (
    role_id   INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    skill_id  INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, skill_id)
);

CREATE TABLE IF NOT EXISTS education (
    id              INTEGER PRIMARY KEY,
    institution     TEXT NOT NULL,
    degree          TEXT NOT NULL,
    field           TEXT,
    focus           TEXT,
    year_completed  INTEGER
);

CREATE TABLE IF NOT EXISTS certifications (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    issuing_org  TEXT,
    year_issued  INTEGER,
    year_expires INTEGER
);

CREATE TABLE IF NOT EXISTS projects (
    id           INTEGER PRIMARY KEY,
    role_id      INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    name         TEXT NOT NULL,
    description  TEXT,
    url          TEXT,
    start_date   TEXT,
    end_date     TEXT,
    tags         TEXT
);

CREATE TABLE IF NOT EXISTS awards (
    id           INTEGER PRIMARY KEY,
    role_id      INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    name         TEXT NOT NULL,
    issuing_org  TEXT,
    year         INTEGER,
    description  TEXT
);

CREATE TABLE IF NOT EXISTS patents (
    id             INTEGER PRIMARY KEY,
    title          TEXT NOT NULL,
    patent_number  TEXT,
    filing_date    TEXT,
    description    TEXT
);

CREATE TABLE IF NOT EXISTS security_clearances (
    id          INTEGER PRIMARY KEY,
    level       TEXT NOT NULL,
    start_year  INTEGER,
    end_year    INTEGER
);

CREATE TABLE IF NOT EXISTS raw_notes (
    id         INTEGER PRIMARY KEY,
    title      TEXT,
    body       TEXT NOT NULL,
    tags       TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
