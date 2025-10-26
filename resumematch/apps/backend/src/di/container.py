import os

from ..core.ports import CandidateRepoPort, VacancyRepoPort, LabelRepoPort, FileStoragePort, MatcherPort
from ..infrastructure.repos import (
    DjangoORMCandidateRepo,
    DjangoORMVacancyRepo,
    DjangoORMLabelRepo,
)
from ..infrastructure.gridfs.storage import MongoGridFSFileStorage
from ..infrastructure.ml.tfidf_matcher import SklearnTfidfMatcher
from ..application.match_usecase import MatchVacancyUseCase
from ..application.label_usecase import LabelCandidateUseCase
from ..interface.graphql.schema import USE_CASES
from ..interface.rest.views import FILE_STORAGE


class Container:
    def __init__(self):
        # Repositories (Django ORM)
        self.candidate_repo: CandidateRepoPort = DjangoORMCandidateRepo()
        self.vacancy_repo: VacancyRepoPort = DjangoORMVacancyRepo()
        self.label_repo: LabelRepoPort = DjangoORMLabelRepo()

        # File storage (MongoDB GridFS)
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.file_storage: FileStoragePort = MongoGridFSFileStorage(mongo_uri)

        # Matcher (Sklearn TF-IDF)
        self.matcher: MatcherPort = SklearnTfidfMatcher(candidate_repo=self.candidate_repo)

        # Use cases
        self.match_vacancy = MatchVacancyUseCase(
            vacancy_repo=self.vacancy_repo, matcher=self.matcher
        )
        self.label_candidate = LabelCandidateUseCase(label_repo=self.label_repo)

    def wire(self):
        # GraphQL use cases
        USE_CASES["match_vacancy"] = self.match_vacancy
        USE_CASES["label_candidate"] = self.label_candidate
        # REST file storage
        global FILE_STORAGE
        FILE_STORAGE = self.file_storage


container = Container()
container.wire()