from typing import Optional

import chromadb


class ChromaService:

    def __init__(self):
        self._client = chromadb.Client()

    def create_collection(self, name: str):
        return self._client.create_collection(name)

    def add_documents(
        self,
        collection_name: str,
        documents: list[dict],
        ids: list[str],
        metadatas: Optional[list[dict]] = None,
    ):
        self._client.add_documents(collection_name, documents, ids, metadatas)
