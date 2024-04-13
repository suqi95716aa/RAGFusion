from typing import List, Iterator, Dict

from rs_core.document.document import Document
from rs_core.loader.unstructured import UnstructuredFileLoader


class PyPDFLoader(UnstructuredFileLoader):
    """Load `PDF` files using `pypdf`.

    You can run the loader in one of two modes: "single" and "elements" and "paged".
    If you use "single" mode, the document will be returned as a single
    RAGFusion Document object. If you use "elements" mode, the unstructured
    library will split the document into elements such as Title and NarrativeText.
    You can pass in additional unstructured kwargs after mode to apply
    different unstructured settings.

    Examples
    --------
    from RAGFusion.document_loaders import PyPDFLoader

    loader = PyPDFLoader(
        "example.pdf", mode="elements", strategy="fast",
    )
    docs = loader.load()

    References
    ----------
    https://unstructured-io.github.io/unstructured/bricks.html#partition-pdf
    """

    def _get_elements(self) -> Dict:
        import pypdf
        reader = pypdf.PdfReader(self.file_path)
        ret = dict()
        for ind, page in enumerate(reader.pages):
            ret[ind] = page.extract_text()
        return ret

    def lazy_load(self) -> Iterator[Document]:
        """Load file."""
        elements = self._get_elements()
        if self.mode == "elements":
            for k, element in elements.items():
                metadata = self._get_metadata()
                # NOTE(MthwRobinson) - the attribute check is for backward compatibility
                # with unstructured<0.4.9. The metadata attributed was added in 0.4.9.
                if hasattr(element, "metadata"):
                    metadata.update(element.metadata.to_dict())
                if hasattr(element, "category"):
                    metadata["category"] = element.category
                yield Document(page_content=str(element), metadata=metadata)

        elif self.mode == "paged":
            # Convert the dict to a list of Document objects
            for k, element in elements.items():
                metadata = self._get_metadata()
                metadata.update({"page_num": k})
                yield Document(page_content=element, metadata=metadata)

        elif self.mode == "single":
            metadata = self._get_metadata()
            text = "\n\n".join([str(content) for k, content in elements.items()])
            yield Document(page_content=text, metadata=metadata)
        else:
            raise ValueError(f"mode of {self.mode} not supported.")