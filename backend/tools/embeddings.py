from openai import OpenAI
from dotenv import load_dotenv
import faiss
import numpy as np

load_dotenv()

class Embeddings:
    def __init__(self):
        self.client = OpenAI()
    
    def embed_text(self, chunks: list[str]):
        vectors = []
        for chunk in chunks:
            embedding = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk
            ).data[0].embedding
            vectors.append(embedding)
        return np.array(vectors).astype("float32")
    
    def build_index(self, vectors: np.array):
        dim = len(vectors[0])
        index = faiss.IndexFlatL2(dim)
        index.add(vectors)
        return index
    
    def search(self, query, index, chunks, top_k=3):
        query_vector = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        ).data[0].embedding
        query_vector = np.array(query_vector).astype("float32").reshape(1, -1)
        distances, indices = index.search(query_vector, top_k)
        return [chunks[i] for i in indices[0]]

