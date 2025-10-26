from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class Label(Enum):
    POS = "pos"
    NEG = "neg"
    LATER = "later"


@dataclass
class SkillsSet:
    items: List[str] = field(default_factory=list)

    def matched_with(self, required: 'SkillsSet') -> List[str]:
        return sorted(set(s.lower() for s in self.items) & set(s.lower() for s in required.items))

    def missing_from(self, required: 'SkillsSet') -> List[str]:
        return sorted(set(s.lower() for s in required.items) - set(s.lower() for s in self.items))


@dataclass
class ExperienceYears:
    value: int


@dataclass
class Location:
    value: str


@dataclass
class Candidate:
    id: str
    full_name: str
    contact_email: Optional[str]
    location: Location
    years_exp: ExperienceYears
    skills: SkillsSet
    resume_file_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Vacancy:
    id: str
    title: str
    location: Optional[Location]
    skills_required: SkillsSet
    jd_text: Optional[str] = None
    jd_file_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MatchScore:
    candidate_id: str
    score: float
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)


@dataclass
class LabelDecision:
    vacancy_id: str
    candidate_id: str
    label: Label
    reason: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)