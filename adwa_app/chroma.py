import os
import dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
BASE_DIR = Path(__file__).resolve().parent.parent

_persist_dir = os.path.join(BASE_DIR, "adwa_app", "chroma_db")

_vector_store = Chroma(
    persist_directory=_persist_dir,
    embedding_function=_embeddings
)

_retriever = _vector_store.as_retriever(search_kwargs={"k": 6})

class Retriever:
    def __init__(self, query):
        self.retrieved = _retriever.invoke(query)
        self.context = "\n\n".join([r.page_content for r in self.retrieved])
    def chroma_result(self):
        print(len(self.retrieved))
        print(f"retrieved: {self.retrieved}\n\n\n")
        meta = []
        for r in self.retrieved:
            meta.append(r.metadata)
        return self.context, meta
