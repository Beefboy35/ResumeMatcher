from dataclasses import dataclass

from ..core.entities import Label, LabelDecision
from ..core.ports import LabelRepoPort


@dataclass
class LabelCandidateUseCase:
    label_repo: LabelRepoPort

    def execute(self, vacancy_id: str, candidate_id: str, label: str, reason: str | None = None) -> None:
        if label not in {Label.POS.value, Label.NEG.value, Label.LATER.value}:
            raise ValueError("Invalid label")
        decision = LabelDecision(
            vacancy_id=vacancy_id,
            candidate_id=candidate_id,
            label=Label(label),
            reason=reason,
        )
        self.label_repo.save(decision)