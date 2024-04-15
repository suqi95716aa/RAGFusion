from unittest import TestCase



class TestSplitter(TestCase):

    def test_text_direct_CharacterTextSplitter(self):

        from rs_splitter import CharacterTextSplitter

        splitter = CharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=70,
            keep_separator=False,
        )

        # read str
        # with open('../doc/新建文本文档.txt', 'r', encoding="utf-8") as f:
        #     content = f.read()
        #     # print(content)
        #     docs_text = splitter.split_text(content)
        #     docs_obj = splitter.create_documents(docs_text, [({"1": "2"}) for _ in range(len(docs_text) + 1)])
        #     for item in docs_obj:
        #         print(">>>>>>>>")
        #         print(item)
        #         print(">>>>>>>>")

        # read document
        from rs_loaders import UnstructuredMarkdownLoader
        loader = UnstructuredMarkdownLoader(
            file_path='../doc/系统架构.md',
            mode="single",  # elements/single/paged
            strategy="fast"
        )
        data = loader.load()
        ret = splitter.split_documents(data)
        print(ret)
        for item in ret:
            print(item)




        # defalut text_splitter
        # print(docs_text)

        # create doc object


    def test_text_direct_RecursiveCharacterTextSplitter(self):

        with open('../doc/新建文本文档.txt', 'r', encoding="utf-8") as f:
            content = f.read()
            # print(content)

        from rs_splitter import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=70,
            keep_separator=False,
            # separators=["10"]

        )

        # defalut text_splitter
        docs_text = splitter.split_text(content)
        # print(docs_text)

        # create doc object
        docs_obj = splitter.create_documents(docs_text, [({"1": "2"}) for _ in range(len(docs_text)+1)])
        for item in docs_obj:
            print(">>>>>>>>>>>>>")
            print(item)
            print(">>>>>>>>>>>>>")


    def test_text_direct_TokenTextSplitter(self):

        with open('../doc/新建文本文档.txt', 'r', encoding="utf-8") as f:
            content = f.read()
            # print(content)

        from rs_splitter import TokenTextSplitter

        # 这里一个token大约由4个字符组成
        splitter = TokenTextSplitter(
            chunk_size=1,
            chunk_overlap=0,
            # separators=["10"]

        )

        text = "what can I do for you dasw dqq whd "

        docs_text = splitter.split_text(text)
        print(docs_text)

        # create doc object
        docs_obj = splitter.create_documents(docs_text, [({"1": "2"}) for _ in range(len(docs_text)+1)])
        for item in docs_obj:
            print(">>>>>>>>>>>>>")
            print(item)
            print(">>>>>>>>>>>>>")

    def test_text_direct_MarkdownTextSplitter(self):

        with open('../doc/系统架构.md', 'r', encoding="utf-8") as f:
            content = f.read()

        from rs_splitter import MarkdownTextSplitter
        splitter = MarkdownTextSplitter(
            chunk_size=500,
            chunk_overlap=10,
        )
        docs_text = splitter.split_text(content)
        docs_obj = splitter.create_documents(docs_text, [({"1": "2"}) for _ in range(len(docs_text)+1)])
        for item in docs_obj:
            print(item)

    def test_text_direct_MarkdownHeaderTextSplitter(self):
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        from rs_splitter import MarkdownHeaderTextSplitter
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            return_each_line=True,
            strip_headers=False,
        )


        # read file
        with open('../doc/系统架构.md', 'r', encoding="utf-8") as f:
            content = f.read()

        docs_text = splitter.split_text(content)
        print(len(docs_text))
        for item in docs_text:
            print(item)


        # read doc
        # from rs_loaders import UnstructuredMarkdownLoader
        # loader = UnstructuredMarkdownLoader(
        #     file_path='../doc/系统架构.md',
        #     mode="single",  # elements/single/paged
        #     strategy="fast"
        # )
        # data = loader.load()

    def test_text_direct_WordHeaderTextSplitter(self):


        from rs_splitter import WordHeaderTextSplitter
        splitter = WordHeaderTextSplitter(
            strip_headers=False,
        )
        data = splitter.split_text(r"F:\编程项目\backend\RAGFusion\doc\福州市长乐区百户村智慧乡村项目-可研暨初设方案v3.5 15.40（20200312）(1).docx")
        #
        for item in data:
            print(item)
            # print(item.page_content[:20], item.metadata)

    def test_text_direct_TextHeaderSplitter(self):

        with open(r"..\doc\新建文本文档.txt", "r", encoding="utf-8") as f:
            content = f.read()

        from rs_splitter import TextHeaderSplitter
        splitter = TextHeaderSplitter()
        data = splitter.split_text([content])
        #
        for item in data:
            print(item)
            # print(item.page_content[:20], item.metadata)

    def test_doc_ParentDocumentSplitter(self):

        with open(r"..\doc\新建文本文档.txt", "r", encoding="utf-8") as f:
            content = f.read()

        from rs_splitter import ParentDocumentSplitter
        from rs_splitter import RecursiveCharacterTextSplitter
        from rs_splitter import TextHeaderSplitter
        splitter = TextHeaderSplitter()
        docs = splitter.split_text([content])

        parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0, add_start_index=True)
        child_splitter = RecursiveCharacterTextSplitter(chunk_size=500,  chunk_overlap=0, add_start_index=True)
        p_splitter = ParentDocumentSplitter(
                            child_splitter=child_splitter,
                            parent_splitter=parent_splitter,
                        )
        p_splitter.split_documents(docs)
