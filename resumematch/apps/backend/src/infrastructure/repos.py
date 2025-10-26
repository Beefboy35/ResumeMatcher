from typing import List, Optional

from ..core.entities import Candidate, Vacancy, LabelDecision, SkillsSet, ExperienceYears, Location
from ..core.ports import CandidateRepoPort, VacancyRepoPort, LabelRepoPort
from .orm.models import CandidateModel, VacancyModel, LabelModel


class DjangoORMCandidateRepo(CandidateRepoPort):
    def get_by_id(self, candidate_id: str) -> Optional[Candidate]:
        try:
            m = CandidateModel.objects.get(id=candidate_id)
            return Candidate(
                id=str(m.id),
                full_name=m.full_name,
                contact_email=m.contact_email,
                location=Location(m.location),
                years_exp=ExperienceYears(m.years_exp),
                skills=SkillsSet(m.skills_json),
                resume_file_id=m.resume_file_id,
            )
        except CandidateModel.DoesNotExist:
            return None

    def list_all(self) -> List[Candidate]:
        res: List[Candidate] = []
        for m in CandidateModel.objects.all():
            res.append(Candidate(
                id=str(m.id),
                full_name=m.full_name,
                contact_email=m.contact_email,
                location=Location(m.location),
                years_exp=ExperienceYears(m.years_exp),
                skills=SkillsSet(m.skills_json),
                resume_file_id=m.resume_file_id,
            ))
        return res

    def save(self, candidate: Candidate) -> None:
        CandidateModel.objects.update_or_create(
            id=candidate.id,
            defaults={
                "full_name": candidate.full_name,
                "contact_email": candidate.contact_email,
                "location": candidate.location.value,
                "years_exp": candidate.years_exp.value,
                "skills_json": candidate.skills.items,
                "resume_file_id": candidate.resume_file_id,
            }
        )


class DjangoORMVacancyRepo(VacancyRepoPort):
    def get_by_id(self, vacancy_id: str) -> Optional[Vacancy]:
        try:
            m = VacancyModel.objects.get(id=vacancy_id)
            return Vacancy(
                id=str(m.id),
                title=m.title,
                location=Location(m.location) if m.location else None,
                skills_required=SkillsSet(m.skills_req_json),
                jd_text=m.jd_text,
                jd_file_id=m.jd_file_id,
            )
        except VacancyModel.DoesNotExist:
            return None

    def save(self, vacancy: Vacancy) -> None:
        VacancyModel.objects.update_or_create(
            id=vacancy.id,
            defaults={
                "title": vacancy.title,
                "location": vacancy.location.value if vacancy.location else None,
                "skills_req_json": vacancy.skills_required.items,
                "jd_text": vacancy.jd_text,
                "jd_file_id": vacancy.jd_file_id,
            }
        )


class DjangoORMLabelRepo(LabelRepoPort):
    def save(self, decision: LabelDecision) -> None:
        v = VacancyModel.objects.get(id=decision.vacancy_id)
        c = CandidateModel.objects.get(id=decision.candidate_id)
        LabelModel.objects.create(
            vacancy=v,
            candidate=c,
            label=decision.label.value,
            reason=decision.reason,
        )