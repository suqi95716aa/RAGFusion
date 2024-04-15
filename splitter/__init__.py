"""**Text Splitters** are classes for splitting text.


**Class hierarchy:**

.. code-block::

    BaseDocumentTransformer --> TextSplitter --> <name>TextSplitter  # Example: CharacterTextSplitter
                                                 RecursiveCharacterTextSplitter -->  <name>TextSplitter

Note: **MarkdownHeaderTextSplitter** and **HTMLHeaderTextSplitter do not derive from TextSplitter.


**Main helpers:**

.. code-block::

    Document, Tokenizer, Language, LineType, HeaderType

"""  # noqa: E501

import importlib
from typing import Any

_module_lookup = {
    "TokenTextSplitter": "splitter.base",
    "TextSplitter": "splitter.base",
    "Tokenizer": "splitter.base",
    "Language": "splitter.base",
    "split_text_on_tokens": "splitter.base",
    "MarkdownTextSplitter": "splitter.character",
    "CharacterTextSplitter": "splitter.character",
    "RecursiveCharacterTextSplitter": "splitter.character",
    "MarkdownHeaderTextSplitter": "splitter.header",
    "WordHeaderTextSplitter": "splitter.header",
    "TextHeaderSplitter": "splitter.header",
    "ParentDocumentSplitter": "splitter.parent",
    "NLTKTextSplitter": "splitter.nltk",
}


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module = importlib.import_module(_module_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = list(_module_lookup.keys())