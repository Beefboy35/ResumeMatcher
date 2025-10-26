from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ...core.entities import MatchScore, SkillsSet, Candidate
from ...core.ports import MatcherPort, CandidateRepoPort


class SklearnTfidfMatcher(MatcherPort):
    def __init__(self, candidate_repo: CandidateRepoPort):
        self.candidate_repo = candidate_repo
        # Для PoC: обучаем в памяти по всем резюме (jd_text не используется)
        self._vectorizer = TfidfVectorizer(max_features=5000)
        self._candidate_texts: list[tuple[str, str, SkillsSet]] = []
        self._matrix = None
        self._fit()

    def _fit(self):
        # Соберём тексты кандидатов из домена (упрощённо: skills как текст)
        candidates: List[Candidate] = self.candidate_repo.list_all()
        self._candidate_texts = [
            (c.id, " ".join(c.skills.items), c.skills) for c in candidates
        ]
        if not self._candidate_texts:
            self._matrix = None
            return
        _, texts, _ = zip(*self._candidate_texts)
        self._matrix = self._vectorizer.fit_transform(list(texts))

    def match(self, vacancy_text: str, top_k: int = 10) -> List[MatchScore]:
        if self._matrix is None or not self._candidate_texts:
            return []
        q = self._vectorizer.transform([vacancy_text])
        sims = cosine_similarity(q, self._matrix).ravel()
        top_idx = np.argsort(sims)[::-1][:top_k]
        results: List[MatchScore] = []
        for idx in top_idx:
            candidate_id, _, skills = self._candidate_texts[idx]
            score = float(sims[idx])
            # Простые правила по навыкам: совпавшие/недостающие между vacancy_text токенами и skills
            vacancy_skills = SkillsSet([w for w in vacancy_text.split() if len(w) > 2])
            matched = skills.matched_with(vacancy_skills)
            missing = skills.missing_from(vacancy_skills)
            reasons = []
            if matched:
                reasons.append(f"Matched skills: {', '.join(matched[:5])}")
            if missing:
                reasons.append(f"Missing skills: {', '.join(missing[:5])}")
            results.append(MatchScore(
                candidate_id=candidate_id,
                score=score,
                matched_skills=matched,
                missing_skills=missing,
                reasons=reasons,
            ))
        return results