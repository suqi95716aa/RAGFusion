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
    "TokenTextSplitter": "rs_splitter.base",
    "TextSplitter": "rs_splitter.base",
    "Tokenizer": "rs_splitter.base",
    "Language": "rs_splitter.base",
    "split_text_on_tokens": "rs_splitter.base",
    "MarkdownTextSplitter": "rs_splitter.character",
    "CharacterTextSplitter": "rs_splitter.character",
    "RecursiveCharacterTextSplitter": "rs_splitter.character",
    "MarkdownHeaderTextSplitter": "rs_splitter.header",
    "WordHeaderTextSplitter": "rs_splitter.header",
    "TextHeaderSplitter": "rs_splitter.header",
    "ParentDocumentSplitter": "rs_splitter.parent",
}


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module = importlib.import_module(_module_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = list(_module_lookup.keys())