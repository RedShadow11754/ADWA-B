import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
_persist_dir = os.path.join(BASE_DIR, "adwa_app", "chroma_db")

# 2. Use Google Embeddings (Uses 0MB of your Render RAM)
# It will automatically look for GEMINI_API_KEY in your environment variables
_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# 3. Initialize Vector Store
_vector_store = Chroma(
    persist_directory=_persist_dir,
    embedding_function=_embeddings
)

# 4. Setup Retriever
_retriever = _vector_store.as_retriever(search_kwargs={"k": 6})

class Retriever:
    def __init__(self, query):
        # We invoke the search immediately upon initialization as per your original logic
        self.retrieved = _retriever.invoke(query)
        self.context = "\n\n".join([r.page_content for r in self.retrieved])

    def chroma_result(self):
        # Useful for debugging in the Render logs
        print(f"Number of docs retrieved: {len(self.retrieved)}")
        
        meta = []
        for r in self.retrieved:
            meta.append(r.metadata)
            
        return self.context, meta