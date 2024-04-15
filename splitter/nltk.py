from __future__ import annotations

from typing import Any, List

from splitter import TextSplitter
from core.document.document import Document


class NLTKTextSplitter(TextSplitter):
    """Using NLTK package to split text"""

    def __init__(
            self,
            separator: str = "\n\n",
            language: str = "english",
            **kwargs: Any
    ) -> None:
        """Initialize the NLTK splitter"""

        super().__init__(**kwargs)
        self._separator = separator
        self._language = language

    def split_text(self, text: str) -> List[Document]:
        try:
            import nltk.tokenize
        except ImportError as e:
            raise ImportError("NLTK package is missing. Install it using `pip install nltk`.") from e

        splits = nltk.tokenize.sent_tokenize(text, language=self._language)
        return self._merge_splits(splits, self._separator)

