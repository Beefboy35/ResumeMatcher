import typing as t
import strawberry

from ...application.match_usecase import MatchVacancyUseCase
from ...application.label_usecase import LabelCandidateUseCase
from ...core.entities import MatchScore

# Простая DI точка для PoC: будет заполнена контейнером
USE_CASES: dict[str, t.Any] = {}


@strawberry.type
class MatchScoreType:
    candidate_id: str
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    reasons: list[str]


@strawberry.type
class Query:
    @strawberry.field
    def match(self, vacancy_id: str, top_k: int = 10) -> list[MatchScoreType]:
        usecase: MatchVacancyUseCase = USE_CASES["match_vacancy"]
        scores: list[MatchScore] = usecase.execute(vacancy_id, top_k=top_k)
        return [
            MatchScoreType(
                candidate_id=s.candidate_id,
                score=s.score,
                matched_skills=s.matched_skills,
                missing_skills=s.missing_skills,
                reasons=s.reasons,
            ) for s in scores
        ]


@strawberry.type
class Mutation:
    @strawberry.field
    def labelCandidate(self, vacancy_id: str, candidate_id: str, label: str, reason: str | None = None) -> bool:
        usecase: LabelCandidateUseCase = USE_CASES["label_candidate"]
        usecase.execute(vacancy_id, candidate_id, label, reason)
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)