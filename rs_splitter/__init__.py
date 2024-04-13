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



from rs_splitter.base import (
    TokenTextSplitter,
    TextSplitter,
    Tokenizer,
    Language,
    split_text_on_tokens
)

from rs_splitter.character import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter
)

from rs_splitter.markdown import (
    MarkdownHeaderTextSplitter,
    MarkdownTextSplitter
)


__all__ = [
    "TokenTextSplitter",
    "TextSplitter",
    "Tokenizer",
    "Language",
    "RecursiveCharacterTextSplitter",
    # "RecursiveJsonSplitter",
    # "LatexTextSplitter",
    # "PythonCodeTextSplitter",
    # "KonlpyTextSplitter",
    # "SpacyTextSplitter",
    # "NLTKTextSplitter",
    "split_text_on_tokens",
    # "SentenceTransformersTokenTextSplitter",
    # "ElementType",
    # "HeaderType",
    # "LineType",
    # "HTMLHeaderTextSplitter",
    "MarkdownHeaderTextSplitter",
    "MarkdownTextSplitter",
    "CharacterTextSplitter",
]

