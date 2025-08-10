import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

class VectorDatabase:
    def __init__(self, db_path="vector_db"):
        self.db_path = db_path
        self.questions = []
        self.answers = []
        self.index = None
        self.embeddings = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def build_or_load(self, json_path, process_log=None):
        emb_path = os.path.join(self.db_path, "embeddings.npy")
        idx_path = os.path.join(self.db_path, "faiss.index")
        qa_path = os.path.join(self.db_path, "qa.json")

        if process_log is not None:
            process_log.append("Checking for existing FAISS index and embeddings...")

        if os.path.exists(emb_path) and os.path.exists(idx_path) and os.path.exists(qa_path) and FAISS_AVAILABLE:
            if process_log is not None:
                process_log.append("Loading FAISS index and embeddings from disk.")
            self.embeddings = np.load(emb_path)
            import faiss
            self.index = faiss.read_index(idx_path)
            with open(qa_path, "r") as f:
                qa = json.load(f)
                self.questions = qa["questions"]
                self.answers = qa["answers"]
        else:
            if process_log is not None:
                process_log.append("Building FAISS index and embeddings from JSON data.")
            with open(json_path, "r") as f:
                data = json.load(f)
            qa_data = data["qa_data"]
            self.questions = [item["question"] for item in qa_data if "question" in item and "answer" in item]
            self.answers = [item["answer"] for item in qa_data if "question" in item and "answer" in item]
            self.embeddings = np.array(self.model.encode(self.questions, show_progress_bar=True))
            if FAISS_AVAILABLE:
                import faiss
                dim = self.embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dim)
                self.index.add(self.embeddings)
                os.makedirs(self.db_path, exist_ok=True)
                np.save(emb_path, self.embeddings)
                faiss.write_index(self.index, idx_path)
                with open(qa_path, "w") as f:
                    json.dump({"questions": self.questions, "answers": self.answers}, f)
                if process_log is not None:
                    process_log.append("FAISS index and embeddings built and saved to disk.")
            else:
                self.index = None
                if process_log is not None:
                    process_log.append("FAISS not available. Using fallback numpy search.")

    def get_top_k(self, query, top_k=5):
        query_vec = self.model.encode([query])
        if FAISS_AVAILABLE and self.index is not None:
            D, I = self.index.search(np.array(query_vec), top_k)
            results = []
            for idx, dist in zip(I[0], D[0]):
                if idx < 0 or idx >= len(self.questions):
                    continue
                sim = 1 / (1 + dist)  # Convert L2 to similarity (optional)
                results.append((idx, sim, {
                    "question": self.questions[idx],
                    "answer": self.answers[idx]
                }))
            return results
        else:
            # Fallback: brute-force cosine similarity
            vectors = self.embeddings
            query_vec = np.array(query_vec)
            vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
            query_vec = query_vec / np.linalg.norm(query_vec)
            similarities = np.dot(vectors, query_vec.T).squeeze()
            top_indices = similarities.argsort()[-top_k:][::-1]
            results = []
            for idx in top_indices:
                results.append((idx, similarities[idx], {
                    "question": self.questions[idx],
                    "answer": self.answers[idx]
                }))
            return results