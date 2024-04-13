from unittest import TestCase



class TestSplitter(TestCase):

    def test_text_direct_CharacterTextSplitter(self):

        with open('../doc/新建文本文档.txt', 'r', encoding="utf-8") as f:
            content = f.read()
            # print(content)

        from rs_splitter import CharacterTextSplitter

        splitter = CharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=70,
            keep_separator=False,
        )

        # defalut text_splitter
        docs_text = splitter.split_text(content)
        # print(docs_text)

        # create doc object
        docs_obj = splitter.create_documents(docs_text, [({"1": "2"}) for _ in range(len(docs_text)+1)])
        for item in docs_obj:
            print(">>>>>>>>")
            print(item)
            print(">>>>>>>>")

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
            print(len(item.page_content))
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
        print(docs_obj)


    def test_text_direct_MarkdownHeaderTextSplitter(self):

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

        with open('../doc/系统架构.md', 'r', encoding="utf-8") as f:
            content = f.read()

        from rs_splitter import MarkdownHeaderTextSplitter
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            return_each_line=False,
            strip_headers=False,
        )
        docs_text = splitter.split_text(content)
        print(len(docs_text))
        for item in docs_text:
            print(item)





