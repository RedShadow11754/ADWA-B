import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Provide your Google API Key
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# 2. Point to your PDF file (Make sure the path is correct!)
loader = PyPDFLoader("your_book_about_adwa.pdf") 
pages = loader.load()

# 3. Break the book into small pieces (Critical for Render's low RAM)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
docs = text_splitter.split_documents(pages)

# 4. Use the GOOGLE "Scanner" (This matches your new chroma.py)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", 
    google_api_key=GOOGLE_API_KEY
)

# 5. Create the NEW chroma_db folder
print("Starting re-indexing... please wait.")
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./adwa_app/chroma_db" # Save it back here
)

print(" Success! Your chroma_db folder is rebuilt and compatible with Google.")