
from langchain.vectorstores import FAISS

class VectorStore:
    @classmethod
    def from_documents(cls, documents, embeddings):
        return FAISS.from_documents(documents, embeddings)
    