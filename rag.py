import faiss
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.embeddings import get_embedding

index = faiss.IndexFlatL2(384)
documents = []

def add_documents(docs):
    global documents
    embeddings = [get_embedding(doc) for doc in docs]
    index.add(np.array(embeddings))
    documents.extend(docs)

def retrieve(query):
    if len(documents) == 0:
        return []

    query_vec = np.array([get_embedding(query)])
    D, I = index.search(query_vec, k=3)
    return [documents[i] for i in I[0]]