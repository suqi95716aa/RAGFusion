from unittest import TestCase


document_texts = ["This is a test document.", "Another test document for demonstration."]


class TestEmbedding(TestCase):

    def test_csv_loader(self):
        from core.embeddings.customize import TestEmbedding

        test_embedding = TestEmbedding(dims="100")

        # 生成文档向量
        document_vectors = test_embedding.to_query_vec(document_texts)
        print("Document vectors:")
        for vector in document_vectors:
            print(vector)

        # 生成查询向量
        query_text = "Query text for embedding."
        query_vector = test_embedding.to_docs_vec(query_text)
        print("\nQuery vector:")
        print(query_vector)






