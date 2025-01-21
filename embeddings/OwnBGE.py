"""
The open source commercial Chinese and English semantic vector model BGE (BAAI General Embedding)
surpasses all similar models in the community in terms of both Chinese and English semantic retrieval accuracy
and overall semantic representation ability, such as OpenAI's text embedding 002. In addition,
BGE maintains the minimum vector dimension in models of the same parameter level, resulting in lower usage costs.

FlagEmbedding: https://github.com/FlagOpen/FlagEmbedding
BGE model link: https://huggingface.co/BAAI/
BGE Code Warehouse: https://github.com/FlagOpen/FlagEmbedding
C-MTEB evaluation benchmark link: https://github.com/FlagOpen/FlagEmbedding/tree/master/benchmark
"""
from __future__ import annotations

import json
import requests
from typing import Optional, Dict, List, Any, Callable

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from requests.exceptions import HTTPError
from pydantic import model_validator, BaseModel

from core.embeddings import Embeddings

# FIX: 用解析文件方式代替
TOKEN: str = "b8d1e618e3e973b4d7b67fe3467ef43c"
BGE_URL: str = "http://116.204.124.212:3222/api/model/bge_call_service/emb_query"


def _create_retry_decorator(embeddings: BGETextEmbedding) -> Callable[[Any], Any]:
    multiplier = 1
    min_seconds = 1
    max_seconds = 4
    # Wait 2^x * 1 second between each retry starting with
    # 1 seconds, then up to 4 seconds, then 4 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(embeddings.max_retries),
        wait=wait_exponential(multiplier, min=min_seconds, max=max_seconds),
        retry=(retry_if_exception_type(HTTPError))
    )


def embed_with_retry(embeddings: BGETextEmbedding, text) -> Any:
    """Use tenacity to retry the embedding call."""
    retry_decorator = _create_retry_decorator(embeddings)

    @retry_decorator
    def _embed_with_retry(text) -> Any:
        try:
            response = requests.post(
                url=BGE_URL,
                headers={
                    "Content-Type": "application/json",
                    "token": embeddings.token
                },
                data=json.dumps({"query": text})
            )
            if response.status_code == 200:
                return json.loads(response.content)["emb"]
            elif response.status_code in [400, 401]:
                # Unreachable Code
                raise ValueError(f"HTTP error occurred: status_code: {response.status_code} \n ")
            else:
                raise HTTPError(
                    f"HTTP error occurred: status_code: {response.status_code} \n "
                )
        except Exception as e:
            # Log the exception or handle it as needed
            raise ValueError(f"Error happen: {str(e)}")

    return _embed_with_retry(text)


# NOTE!! Without Public URL to use, just build myself
class BGETextEmbedding(Embeddings, BaseModel):

    """
    Using BGE model to embed text.

    Exeample Code:

        from embeddings import BGETextEmbedding
        data = {
            "token": ""
            "max_retries": 5
        }
        emb = BGETextEmbedding(**data)
        vec = emb.to_docs_vec("I wanna test")
    """

    """Initial header in the embedding"""
    token: Optional[str] = TOKEN
    """Set max retry nums, default 2"""
    max_retries: Optional[int] = 2

    @model_validator(mode="before")
    @classmethod
    def validate_env(cls, data: Any) -> Any:
        return data

    def _emb(self, text: str) -> Optional[List[float]]:
        """Embed method"""
        try:
            response = requests.post(
                url=self.url,
                headers=self.header,
                data=json.dumps({"query": text})
            )
            if response.status_code == 200:
                return json.loads(response.content)["emb"]
            elif response.status_code in [400, 401]:
                # Unreachable Code
                raise ValueError(f"HTTP error occurred: status_code: {response.status_code} \n ")
            else:
                raise HTTPError(
                    f"HTTP error occurred: status_code: {response.status_code} \n "
                )
        except Exception as e:
            # Log the exception or handle it as needed
            raise HTTPError(f"Error happen: {str(e)}")

    def embed_query(self, text: str) -> List[float]:
        """
        Multi text callable method

        Args:
            texts: The texts to embed.

        Returns:
            Embedding for the texts.

        """
        # embedding = embed_with_retry(self, )

        return embed_with_retry(self, text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Single text callable method

        Args:
            text: The text to embed.

        Returns:
            Embedding for the text.
        """
        return [embed_with_retry(self, text) for text in texts]









