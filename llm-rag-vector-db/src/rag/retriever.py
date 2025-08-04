from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self):
        self.database = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def set_database(self, db):
        self.database = db

    def retrieve(self, query, top_k=3):
        query_vector = self.model.encode(query)
        return self.database.get_top_k_vectors(query_vector, top_k)