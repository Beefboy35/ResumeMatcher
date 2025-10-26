from dataclasses import dataclass
from typing import List

from ..core.entities import MatchScore
from ..core.ports import VacancyRepoPort, MatcherPort


@dataclass
class MatchVacancyUseCase:
    vacancy_repo: VacancyRepoPort
    matcher: MatcherPort

    def execute(self, vacancy_id: str, top_k: int = 10) -> List[MatchScore]:
        vacancy = self.vacancy_repo.get_by_id(vacancy_id)
        if not vacancy or not (vacancy.jd_text or vacancy.jd_file_id):
            return []
        text = vacancy.jd_text or ""
        # В проде: если jd_file_id, загрузить текст из хранилища
        results = self.matcher.match(text, top_k=top_k)
        return results