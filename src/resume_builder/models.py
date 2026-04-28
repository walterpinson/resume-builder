from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Company:
    id: Optional[int]
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None


@dataclass
class Role:
    id: Optional[int]
    company_id: int
    title: str
    employment_type: Optional[str] = None
    start_date: str = ""
    end_date: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[str] = None
    summary: Optional[str] = None


@dataclass
class Accomplishment:
    id: Optional[int]
    role_id: int
    description: str
    metric: Optional[str] = None
    impact_area: Optional[str] = None
    tags: Optional[str] = None
    weight: int = 3


@dataclass
class Skill:
    id: Optional[int]
    name: str
    category: Optional[str] = None
    proficiency: Optional[str] = None
    last_used_year: Optional[int] = None
    years_experience: Optional[int] = None


@dataclass
class Education:
    id: Optional[int]
    institution: str
    degree: str
    field: Optional[str] = None
    focus: Optional[str] = None
    year_completed: Optional[int] = None


@dataclass
class Certification:
    id: Optional[int]
    name: str
    issuing_org: Optional[str] = None
    year_issued: Optional[int] = None
    year_expires: Optional[int] = None


@dataclass
class Project:
    id: Optional[int]
    name: str
    role_id: Optional[int] = None
    description: Optional[str] = None
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    tags: Optional[str] = None


@dataclass
class Award:
    id: Optional[int]
    name: str
    role_id: Optional[int] = None
    issuing_org: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None


@dataclass
class Patent:
    id: Optional[int]
    title: str
    patent_number: Optional[str] = None
    filing_date: Optional[str] = None
    description: Optional[str] = None


@dataclass
class SecurityClearance:
    id: Optional[int]
    level: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None


@dataclass
class RawNote:
    id: Optional[int]
    body: str
    title: Optional[str] = None
    tags: Optional[str] = None
    created_at: Optional[str] = None
