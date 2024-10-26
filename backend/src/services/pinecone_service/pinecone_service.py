import os
from typing import Optional

import backoff
from pinecone import Pinecone
from pinecone.exceptions import ServiceException
from src.services.pinecone.utils import already_exists_error


class PineconeService:

    def __init__(self):
        self._pinecone = Pinecone()
        self._index_name = os.getenv("PINECONE_INDEX_NAME")
        self._index = self._pinecone.Index(self._index_name)

    @backoff.on_exception(
        backoff.expo,
        ServiceException,
        jitter=backoff.random_jitter,
        giveup=already_exists_error,
    )
    def upsert_index(self, vectors, namespace: Optional[str] = None):
        self._index.upsert(vectors=vectors, namespace=namespace)

    def query_index(
        self,
        top_k: int,
        vector,
        namespace: Optional[str] = None,
        include_metadata: bool = True,
    ):
        query_resp = self._index.query(
            top_k=top_k,
            vector=vector,
            namespace=namespace,
            include_metadata=include_metadata,
        )
        return {"matches": query_resp["matches"]}
