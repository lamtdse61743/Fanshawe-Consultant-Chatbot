from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
import pickle

class VectorDatabase:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None

    def load_from_json(self, items, index_path="faiss.index", meta_path="faiss_meta.pkl"):
        # Try to load FAISS index and metadata from disk
        if os.path.exists(index_path) and os.path.exists(meta_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                meta = pickle.load(f)
                self.questions = meta["questions"]
                self.answers = meta["answers"]
            print(f"Loaded FAISS index and metadata from disk.")
            return

        # Otherwise, build index and save to disk
        vectors = []
        for item in items:
            question = item.get('question', '')
            answer = item.get('answer', 'No answer provided.')
            vector = self.model.encode(question)
            vectors.append(vector)
            self.questions.append(question)
            self.answers.append(answer)
        vectors = np.array(vectors).astype('float32')
        self.index = faiss.IndexFlatIP(vectors.shape[1])  # Inner product (cosine if normalized)
        faiss.normalize_L2(vectors)  # Normalize for cosine similarity
        self.index.add(vectors)
        faiss.write_index(self.index, index_path)
        with open(meta_path, "wb") as f:
            pickle.dump({"questions": self.questions, "answers": self.answers}, f)
        print(f"Built and saved FAISS index and metadata to disk.")

    def get_top_k_vectors(self, query_vector, top_k=3):
        if self.index is None:
            return []
        query_vector = np.array(query_vector).astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_vector)
        scores, indices = self.index.search(query_vector, top_k)
        results = []
        for rank, idx in enumerate(indices[0]):
            results.append((idx, scores[0][rank], {
                'question': self.questions[idx],
                'answer': self.answers[idx]
            }))
        return results