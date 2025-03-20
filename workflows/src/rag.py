from sentence_transformers import SentenceTransformer
import faiss
from transformers.pipelines import pipeline
import numpy as np

class Rag:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.IndexFlatL2(384)  # dimension 384 pour all-MiniLM-L6-v2
    generator = pipeline('text-generation', model='distilgpt2')  # Modèle léger GPT2 distillé

    def chunk_text(self, content, chunk_size=500, overlap=50):
        """
        Chunk text
        :param content:
        :param chunk_size:
        :param overlap:
        :return:
        """
        chunks = []
        for item in content:
            text = item["text"]
            for i in range(0, len(text), chunk_size - overlap):
                chunks.append({
                    "page": item["page"],
                    "polygon": item["polygon"],
                    "text": text[i:i + chunk_size],
                    "content_type": item["content_type"]
                })
        return chunks

    def embed_chunks(self, chunks: int, embedder: SentenceTransformer):
        """
        Embed chunks and index them on faiss Index
        :param chunks:
        :param embedder:
        :return:
        """
        embeddings = embedder.encode([chunk["text"] for chunk in chunks])
        self.index.add(embeddings)
        return embeddings

    # Étape 4: Recherche hybride (sémantique et vectorielle)
    def semantic_search(self, question, chunks, k=3):
        """
        Sementic research with faiss
        :param question:
        :param chunks:
        :param k:
        :return:
        """
        question_embedding = self.embedder.encode([question])
        distances, indices = self.index.search(question_embedding, k)
        return [(chunks[idx], distances[0][i]) for i, idx in enumerate(indices[0])]

    def vector_search(self, question, chunks, k=3):
        """
        Reshearch based on vector
        :param question:
        :param chunks:
        :param k:
        :return:
        """
        question_embedding = self.embedder.encode([question])
        distances = []
        for chunk in chunks:
            chunk_embedding = self.embedder.encode([chunk["text"]])
            distance = np.linalg.norm(question_embedding - chunk_embedding)
            distances.append(distance)
        sorted_idx = np.argsort(distances)[:k]
        return [(chunks[idx], distances[idx]) for idx in sorted_idx]

    def generate_response(self, question, context_chunks, scores, generator: pipeline):
        """
        Reformule the response with an LLM to get a clean response
        :param question:
        :param context_chunks:
        :param scores:
        :param generator:
        :return:
        """
        context = " ".join(chunk["text"] for chunk in context_chunks)
        prompt = f"Contexte : {context}\nQuestion : {question}\nRéponse :"
        response = generator(prompt, max_length=200)
        return response[0]['generated_text'], scores