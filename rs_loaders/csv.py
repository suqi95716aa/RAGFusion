import csv
import os
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, Iterator, Optional, Sequence, Union

from rs_core.document.document import Document
from rs_core.loader.loader import BaseLoader
from rs_utils.document.helpers import detect_file_encodings


class CSVLoader(BaseLoader):
    """Load a `CSV` file into a list of Documents.

    Each document represents one row of the CSV file. Every row is converted into a
    key/value pair and outputted to a new line in the document's page_content.

    The source for each document loaded from csv is set to the value of the
    `file_path` argument for all documents by default.
    You can override this by setting the `source_column` argument to the
    name of a column in the CSV file.
    The source of each document will then be set to the value of the column
    with the name specified in `source_column`.

    Output Example:
        Document(page_content=text, metadata={'source': 'qa-template.csv', 'row': 0})
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        source_column: Optional[str] = None,
        metadata_columns: Sequence[str] = (),
        csv_args: Optional[Dict] = None,
        encoding: Optional[str] = None,
        autodetect_encoding: bool = False,
    ):
        """

        Args:
            file_path: The path to the CSV file.
            source_column: The name of the column in the CSV file to use as the source.
              Optional. Defaults to None.
            metadata_columns: A sequence of column names to use as metadata. Optional.
            csv_args: A dictionary of arguments to pass to the csv.DictReader.
              Optional. Defaults to None.
            encoding: The encoding of the CSV file. Optional. Defaults to None.
            autodetect_encoding: Whether to try to autodetect the file encoding.
        """
        self.file_path = file_path
        self.source_column = source_column
        self.metadata_columns = metadata_columns
        self.encoding = encoding
        self.csv_args = csv_args or {}
        self.autodetect_encoding = autodetect_encoding

    def lazy_load(self) -> Iterator[Document]:
        try:
            # 打开文件并处理
            with open(self.file_path, newline="", encoding=self.encoding) as csvfile:
                yield from self.__read_file(csvfile)
        except UnicodeDecodeError as e:
            if self.autodetect_encoding:
                detected_encodings = detect_file_encodings(self.file_path)
                for encoding in detected_encodings:
                    try:
                        with open(self.file_path, newline="", encoding=encoding.encoding) as csvfile:
                            yield from self.__read_file(csvfile)
                            break
                    except UnicodeDecodeError:
                        continue
            else:
                raise RuntimeError(f"Error loading {self.file_path}") from e
        except Exception as e:
            raise RuntimeError(f"Error loading {self.file_path}") from e

    def __read_file(self, csvfile: TextIOWrapper) -> Iterator[Document]:
        csv_reader = csv.DictReader(csvfile, **self.csv_args)
        for ind, row in enumerate(csv_reader):
            try:
                sources = {
                    "source": row[self.source_column]
                    if self.source_column is not None
                    else os.path.basename(str(self.file_path)),
                    "prefix_type": os.path.basename(str(self.file_path)).split(".")[1]
                    if self.file_path and "." in str(self.file_path)
                    else "Unknow File Type"
                }
            except KeyError:
                raise ValueError(
                    f"Source column '{self.source_column}' not found in CSV file."
                )

            metadata = {**sources, "row": ind}
            for col in self.metadata_columns:
                try:
                    metadata[col] = row[col]
                except KeyError:
                    raise ValueError(f"Metadata column '{col}' not found in CSV file.")

            content = "\n".join(
                f"{k.strip()}: {v.strip() if v is not None else v}"
                for k, v in row.items()
                if k not in self.metadata_columns
            )

            yield Document(page_content=content, metadata=metadata)


