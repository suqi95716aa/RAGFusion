from abc import ABC
from typing import List, Any


class Serializable(ABC):
    """Serializable document object base class."""

    def __init__(self, page_content: str, metadata: dict, **kwargs: Any) -> None:
        self._rs_metadata = metadata
        self._rs_page_content = page_content

    @classmethod
    def is_rs_serializable(cls) -> bool:
        """Is this class serializable?"""
        return False

    @classmethod
    def get_rs_namespace(cls) -> List[str]:
        """Get the namespace of the RAGFusion object.

        For example, if the class is `RAGFusion.rs_core.serializable.Serializable`, then the
        namespace is ["RAGFusion", "rs_core", "documents"]
        """
        return cls.__module__.split(".")

    def to_json(self):
        """transfer this object to json"""
        pass

    def __str__(self):
        if self.is_rs_serializable():
            return f"{self.__class__.__name__}(page_content={self._rs_page_content}, metadata={self._rs_metadata})"

        import warnings
        warnings.warn(f"Cant't serialize this document")
        return f'<{self.__class__.__name__} object at {hex(id(self))}>'

