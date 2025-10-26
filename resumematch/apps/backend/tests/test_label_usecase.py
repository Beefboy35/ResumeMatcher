import pytest

from src.application.label_usecase import LabelCandidateUseCase
from src.core.entities import Label, LabelDecision
from src.core.ports import LabelRepoPort


class InMemoryLabelRepo(LabelRepoPort):
    def __init__(self):
        self.saved: list[LabelDecision] = []

    def save(self, decision: LabelDecision) -> None:
        self.saved.append(decision)


def test_label_usecase_valid_label():
    repo = InMemoryLabelRepo()
    uc = LabelCandidateUseCase(label_repo=repo)
    uc.execute("vac-1", "cand-1", Label.POS.value, reason="good fit")
    assert len(repo.saved) == 1
    assert repo.saved[0].label == Label.POS


def test_label_usecase_invalid_label():
    repo = InMemoryLabelRepo()
    uc = LabelCandidateUseCase(label_repo=repo)
    with pytest.raises(ValueError):
        uc.execute("vac-1", "cand-1", "bad_label")