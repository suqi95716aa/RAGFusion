import random
import uuid
from unittest import TestCase

from vectorstore.milvus import Milvus
from embeddings.OwnBGE import BGETextEmbedding

# Create BGE Initial Params
embedding_function = BGETextEmbedding()
# Create collection_name
collection_name = "articleStore"
# Create collection_description
collection_description = "It is a collection of storage article vector for retrieve."
# Create collection_properties
collection_properties = {
    "collection.ttl.seconds": 60
}
# Create connection_args
# MILVUS_CONNECTION = {
#     "host": "8.134.201.130",
#     "port": "19530",
#     "user": "",
#     "password": "",
#     "secure": False,
# }
MILVUS_CONNECTION = {
    "host": "111.229.88.79",
    "port": "19530",
    "user": "",
    "password": "",
    "secure": False,
}
# Create consistency_level
consistency_level = "Strong"
# Create index_params
INDEX_PARAMS = {
    "index_type": "IVF_FLAT",
    "metric_type": "IP",
    "params": {"nlist": 10},
}
# Create search_params
search_params = {"IVF_FLAT": {"metric_type": "IP", "params": {"nlist": 10}}}
# Create drop_old
drop_old = False
# Create auto_id
auto_id = False
# Create primary_field
primary_field = "child_id"
# Create text_field
text_field = "text"
# Create vector_field
vector_field = "text_vector"
# Create metadata_field
metadata_field = None
# Create partition_key_field
partition_key_field = "article_id"
# Create replica_number
replica_number = 1


class TestMilvus(TestCase):

    def test_milvus(self):
        from vectorstore.milvus import Milvus
        from embeddings.OwnBGE import BGETextEmbedding

        '''Create BGE Initial Params'''
        BGE_EMB = BGETextEmbedding()

        '''Create Milvus Connection Params'''
        # embedding_function：embedding对象，实现了emb能力
        EMBEDDING_FUNCTION = BGE_EMB

        # collection_name：集合名称
        COLLECTION_NAME = "TEST_UPLOAD"

        # collection_description： 集合描述
        COLLECTION_DESCRIPTION = "TEST"

        # collection_properties：MILVUS集合属性，目前只支持修改ttl
        MILVUS_COLLECTION_PROPERTIES = {
            "collection.ttl.seconds": 60
        }

        # connection_args：创建MILVUS连接
        MILVUS_CONNECTION = {
            "host": "8.134.201.130",
            "port": "19530",
            "user": "",
            "password": "",
            "secure": False,
        }

        # consistency_level: 一致性等级,有Strong, Bounded, Eventually, Session, Customized.
        CONSISTENCY_LEVEL = "Session"

        """
        index_params 是一个字典，用于在 Milvus 中配置索引参数。下面是它的组成部分的中文解释：
        metric_type: 这指定了用于计算距离的度量类型。在这个例子中，它被设置为 "L2"，代表欧几里得距离。其他常见的选择包括 "IP" 用于内积或 "COSINE" 用于余弦相似度。
        index_type: 这指定了要构建的索引类型。在这个例子中，它被设置为 "HNSW"，代表层次导航小世界（Hierarchical Navigable Small World）索引。这是一种近似最近邻（ANN）索引，设计用于高维数据，相比于精确搜索，它在效率和性能上有优势。
        params: 这是一个字典，包含特定于索引类型的额外参数。对于 HNSW，参数包括： 
        M: 这是图中每个点的连接数。值越高，索引的准确性越高，但索引的大小也会增加。
        efConstruction: 这是在索引构建过程中用于动态列表的尺寸。值越高，索引的准确性越高，但索引构建的时间也会增加。
        """
        # index_params：索引构建参数
        INDEX_PARAMS = {
                           "index_type": "AUTOINDEX",
                           "metric_type": "L2",
                           "params": {"M": 8, "efConstruction": 64},
                       } or \
                       {
                           "index_type": "IVF_FLAT",
                           "metric_type": "IP",
                           "params": {"nlist": 20},
                       }

        # search_params：索引查询参数,ip(consine)适用文本场景
        SEARCH_PARAMS = {"IVF_FLAT": {"metric_type": "IP", "params": {"nlist": 20}}}

        # drop_old：丢弃索引，重新创建
        DROP_ID = False

        # primary_field：主键
        PRIMARY_KEY = "pk"

        # Text字段：可以指定创建一个text字段
        TEXT_FIELD = "text"

        # metadata_field：只有当metadata_field为空时，add_texts中添加metadatas会作为每个具体的字段
        # 如果metadata_field不为空，则会整个metadate会作为json
        """
        如果 self._metadata_field 为 None，这意味着元数据不会被存储在单独的字段中，而是会被映射到其他字段上。这通常是为了方便查询和过滤，因为元数据可以作为向量数据的附加信息。
        在这种情况下，代码会遍历 metadatas 列表中的每个元数据字典，并将每个字典中的键值对添加到 insert_dict 中对应的字段列表中。这里的 keys 列表是根据 self.auto_id 的值来确定的，如果 self.auto_id 为 True，那么 keys 将包含除了主键字段之外的所有字段名；如果 self.auto_id 为 False，keys 将包含所有字段名。
        这样，每个元数据字典中的键值对都会被添加到相应的字段列表中，这样在查询时就可以根据这些字段的值来过滤和检索向量数据。
        例如，如果 metadatas 列表中的一个元数据字典是 {'age': 30, 'gender': 'male'}，并且 self.fields 包含 'age' 和 'gender' 字段，那么这两个键值对将被添加到 insert_dict 中的相应列表中。这样，你就可以根据这些元数据字段来查询和过滤向量数据了。
        """
        METADATA_FIELD = "meta" or None

        # partition_key_field：分区字段，选用哪个key分区
        PARTITION_KEY_FIELD = "P_F"

        # vector_field：向量字段，选取哪个字段做向量字段
        VECTOR_FIELD = "userid"

        # partition_names：指定用于加载哪些分区
        PRATITION_NAME = ["user_123", "user_456"]

        milvus_store = Milvus(
            embedding_function=BGE_EMB,
            collection_name="TestUploadDoc",
            drop_old=False,
        )

    def test_milvus_create_index(self):
        milvus_store = Milvus(
            embedding_function=embedding_function,
            collection_name=collection_name,
            collection_description=collection_description,
            collection_properties=collection_properties,
            connection_args=MILVUS_CONNECTION,
            consistency_level=consistency_level,
            index_params=INDEX_PARAMS,
            search_params=search_params,
            drop_old=drop_old,
            auto_id=auto_id,
            primary_field=primary_field,
            text_field=text_field,
            vector_field=vector_field,
            metadata_field=metadata_field,
            partition_key_field=partition_key_field,
            # partition_names = replica_number,
            replica_number=replica_number,
            timeout=None,
        )

        # read file and split
        with open(r"../../doc/新建文本文档.txt", "r", encoding="utf-8") as f:
            content = f.read()

        from splitter import ParentDocumentSplitter
        from splitter import RecursiveCharacterTextSplitter
        from splitter import TextHeaderSplitter
        splitter = TextHeaderSplitter()
        docs = splitter.split_text([content])

        parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0, add_start_index=True)
        child_splitter = RecursiveCharacterTextSplitter(chunk_size=500,  chunk_overlap=0, add_start_index=True)
        p_splitter = ParentDocumentSplitter(
                            child_splitter=child_splitter,
                            parent_splitter=parent_splitter,
                        )
        parent_document, child_document = p_splitter.split_documents(docs)

        article_id = uuid.uuid4()
        texts = [child.page_content for child in child_document]
        ids = [child.metadata.get("child_id") for child in child_document]
        metadatas = [{"article_id": str(article_id), "parent_id": child.metadata.get("parent_id")} for child in child_document]

        # print(texts)
        # print(ids)
        # print(metadatas)

        # 不需要提供向量字段，会自动emb texts
        ret = milvus_store.add_texts(
            texts=texts,   # text_field、vector_field
            metadatas=metadatas,  # 对应text，可拓展的，但是需要和提供的text字段不一样
            ids=ids # child_id
        )
        print(ret)

    def test_check_all_data_in_index(self):
        from pymilvus import (
            connections,
            utility,
            CollectionSchema,
            Collection,
        )
        from uuid import uuid4

        alias = uuid4().hex
        connections.connect(alias=alias, **MILVUS_CONNECTION)

        col = Collection(
            collection_name,
            using=alias,
        )

        search_params = {
            "metric_type": "IP",
            "params": {"nprobe": 1}
        }

        query_expression = "text1 == '234111'"

        results = col.search(
            data=[[random.random() for _ in range(1024)]],
            anns_field=vector_field,
            limit=20,
            expr=query_expression,
            param=search_params,
            output_fields=[primary_field, text_field, vector_field]
        )

        for hits in results:
            for hit in hits:
                # print(hit)
                print(f"hit: {hit}, query field: {hit.entity.get(primary_field)}, sql field: {hit.entity.get(text_field)}")
            print("\n")

        # results = col.query(expr=query_expression)
        #
        # for hits in results:
        #     print(hits)
        #     print("\n")





