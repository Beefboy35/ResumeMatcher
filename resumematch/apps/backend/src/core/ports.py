from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import Candidate, Vacancy, LabelDecision, MatchScore


class CandidateRepoPort(ABC):
    @abstractmethod
    def get_by_id(self, candidate_id: str) -> Optional[Candidate]:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Candidate]:
        raise NotImplementedError

    @abstractmethod
    def save(self, candidate: Candidate) -> None:
        raise NotImplementedError


class VacancyRepoPort(ABC):
    @abstractmethod
    def get_by_id(self, vacancy_id: str) -> Optional[Vacancy]:
        raise NotImplementedError

    @abstractmethod
    def save(self, vacancy: Vacancy) -> None:
        raise NotImplementedError


class LabelRepoPort(ABC):
    @abstractmethod
    def save(self, decision: LabelDecision) -> None:
        raise NotImplementedError


class MatcherPort(ABC):
    @abstractmethod
    def match(self, vacancy_text: str, top_k: int = 10) -> List[MatchScore]:
        """Возвращает топ-K кандидатов согласно модели."""
        raise NotImplementedError


class FileStoragePort(ABC):
    @abstractmethod
    def put_file(self, filename: str, content: bytes) -> str:
        """Сохраняет файл и возвращает file_id."""
        raise NotImplementedError

    @abstractmethod
    def get_file(self, file_id: str) -> bytes:
        raise NotImplementedError