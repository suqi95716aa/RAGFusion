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
import json
import requests
from typing import Optional, Dict, List, Any

from pydantic import model_validator, BaseModel

from core.embeddings import Embedding

# FIX: 用解析文件方式代替
# Basic params
CONTENT_TYPE: str = "application/json"
TOKEN: str = "b8d1e618e3e973b4d7b67fe3467ef43c"
BGE_URL: str = "http://116.204.124.212:32222/api/model/bge_call_service/emb_query"


# NOTE!! Without Public URL to use, just build myself
class BGETextEmbedding(BaseModel, Embedding):

    """
    Using BGE model to embed text.

    Exeample Code:

        from embeddings import BGETextEmbedding

        data = {
            "header": {"Header text": "!"},
            "url": "URL text"
        }
        emb = BGETextEmbedding(**data)
        # test to_docs_vec
        vec = emb.to_docs_vec("123")
    """

    # Model use header
    header: Optional[Dict] = None
    # Model use URL
    url: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def validate_relative_env(cls, values: Any) -> Any:
        """Enrich params that send request need"""
        values["header"] = {"Content-Type": CONTENT_TYPE, "token": TOKEN}
        values["url"] = BGE_URL
        return values

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
            else:
                # Unreachable Code
                print(  # noqa: T201
                    f"""Error: Received status code {response.status_code} from 
                    embedding API"""
                )
                return None

        except Exception as e:
            # Log the exception or handle it as needed
            print(f"Exception occurred while trying to get embeddings: {str(e)}")  # noqa: T201
            return None

    def to_query_vec(self, texts: List[str]) -> List[List[float]]:
        """Single text callable method"""
        return [self._emb(text=text) for text in texts]

    def to_docs_vec(self, text: str) -> List[float]:
        """Multi text callable method"""
        return self._emb(text=text)









