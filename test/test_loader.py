from unittest import TestCase


class TestLoader(TestCase):

    def test_csv_loader(self):
        from loaders import CSVLoader
        # 详细参数可观察csv build in
        loader = CSVLoader(file_path='../doc/qa-template.csv', csv_args={
            'delimiter': ',',
            'quotechar': '"',
            # 'fieldnames': ['MLB Team', 'Payroll in millions', 'Wins']
        })
        data = loader.load()
        for item in data:
            print(item)

    def test_excel_loader(self):
        from loaders import ExcelLoader
        # 详细参数可观察csv build in
        # loader = ExcelLoader(
        #     file_path='../doc/qa-template.xlsx',
        #     source_column="query",        # 当前行数据的数据来源，以具体的数据代表
        #     metadata_columns=("query",)   # 在excel cols中的元数据，不充当数据源
        # )
        loader = ExcelLoader(
            file_path='../doc/副本副本流程助手终版校验final666.xlsx',
        )
        data = loader.load()
        for item in data:
            print(item)

    def test_markdown_loader(self):
        from loaders import UnstructuredMarkdownLoader
        # TODO: Support header
        loader = UnstructuredMarkdownLoader(
            file_path='../doc/系统架构.md',
            mode="single",  # elements/single/paged
            strategy="fast"
        )
        data = loader.load()
        for item in data:
            print(item.metadata)

    def test_word_loader(self):
        from loaders import UnstructuredWordDocumentLoader
        # TODO: Support header
        loader = UnstructuredWordDocumentLoader(
            "../doc/附件10 整体服务方案.doc",
            mode="paged",  # elements/single/paged
            strategy="fast"
        )

        data = loader.load()
        print(len(data))
        for item in data: print(item)

    def test_async_word_loader(self):
        from loaders import UnstructuredWordDocumentLoader
        import asyncio
        # TODO: Support header
        loader = UnstructuredWordDocumentLoader(
            "../doc/附件10 整体服务方案.doc",
            mode="paged",  # elements/single/paged
            strategy="fast"
        )
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(loader.aload())
        print(str(data[0]))
        # for item in data: print(item)

    def test_pdf_loader(self):
        from loaders import PyPDFLoader
        # TODO: Support header
        loader = PyPDFLoader(
            "../doc/test.pdf",
            mode="paged",  # elements/single/paged
            strategy="fast"
        )

        data = loader.load()
        for item in data:
            print(item)

    def test_async_pdf_loader(self):
        from loaders import PyPDFLoader
        import asyncio

        loader = PyPDFLoader(
            "../doc/test.pdf",
            mode="paged",  # elements/single/paged
            strategy="fast"
        )
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(loader.aload())
        print(data)
        for item in data:
            print(item)






