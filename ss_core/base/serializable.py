from abc import ABC
from typing import List, Any


class Serializable(ABC):
    """Serializable document object base class."""

    def __init__(self, page_content: str, metadata: dict, **kwargs: Any) -> None:
        self._ss_metadata = metadata
        self._ss_page_content = page_content

    @classmethod
    def is_ss_serializable(cls) -> bool:
        """Is this class serializable?"""
        return False

    @classmethod
    def get_ss_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object.

        For example, if the class is `superSplitter.ss_core.serializable.Serializable`, then the
        namespace is ["superSplitter", "ss_core", "documents"]
        """
        return cls.__module__.split(".")

    def to_json(self):
        """transfer this object to json"""
        pass

    def __str__(self):
        if self.is_ss_serializable():
            return f"{self.__class__.__name__}(page_content={self._ss_page_content}, metadata={self._ss_metadata})"

        import warnings
        warnings.warn(f"Cant't serialize this document")
        return f'<{self.__class__.__name__} object at {hex(id(self))}>'

