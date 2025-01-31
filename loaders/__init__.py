"""**Document Loaders**  are classes to load Documents.

**Document Loaders** are usually used to load a lot of Documents in a single run.

**Class hierarchy:**

.. code-block::

    BaseLoader --> <name>Loader  # Examples: TextLoader, UnstructuredFileLoader

"""
import importlib
from typing import Any

_module_lookup = {
    "CSVLoader": "loaders.csv",
    "ExcelLoader": "loaders.excel",
    "PyPDFLoader": "loaders.pdf",
    "UnstructuredMarkdownLoader": "loaders.markdown",
    "UnstructuredWordDocumentLoader": "loaders.word",
}


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module = importlib.import_module(_module_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = list(_module_lookup.keys())
