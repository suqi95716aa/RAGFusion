from abc import ABC, abstractmethod
from typing import List

from core.runnables.sync import run_in_executor


class Embedding(ABC):
    """Embedding base model"""

    @abstractmethod
    def to_query_vec(self, texts: List[str]) -> List[List[float]]:
        """embed query"""

    @abstractmethod
    def to_docs_vec(self, text: str) -> List[float]:
        """embed documents"""

    async def ato_query_vec(self, texts: str) -> List[float]:
        """Asynchronous embed query to vec"""
        return await run_in_executor(None, self.to_query_vec, texts)

    async def ato_docs_vec(self, texts: str) -> List[float]:
        """Asynchronous embed documents to vec"""
        return await run_in_executor(None, self.to_docs_vec, texts)