from typing import Optional
from pymongo import MongoClient
from gridfs import GridFS

from ...core.ports import FileStoragePort


class MongoGridFSFileStorage(FileStoragePort):
    def __init__(self, mongo_uri: str, db_name: str = "resumematch"):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.fs = GridFS(self.db)

    def put_file(self, filename: str, content: bytes) -> str:
        file_id = self.fs.put(content, filename=filename)
        return str(file_id)

    def get_file(self, file_id: str) -> bytes:
        gridout = self.fs.get(file_id)
        return gridout.read()