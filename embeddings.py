from pinecone import Pinecone
import re
import openai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import numpy as np


load_dotenv()


# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
EMBEDDINGS_MODEL = "text-embedding-ada-002"
embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Define the index name
index_name = os.getenv('PINECONE_INDEX')

# Instantiate the index
index = pc.Index(index_name)

# Chunk size
chunk_size = 1000

def preprocess_text(text):
    # Replace consecutive spaces, newlines, and tabs
    text = re.sub(r'\s+', ' ', text)
    return text

def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    # load your data
    data = loader.load()
    # Split your data up into smaller documents with Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    documents = text_splitter.split_documents(data)
    # Convert Document objects into strings
    texts = [str(doc) for doc in documents]
    return texts

def create_embeddings(texts):
   embeddings = []
   for text in texts:
        embedding = embeddings_model.embed_documents(text, chunk_size)[0]
        embeddings.append({
            "embedding": embedding,
            "text": text
        })
   return embeddings

def get_ids_from_query(index,input_vector):
  results = index.query(vector=input_vector, top_k=10000,include_values=False)
  ids = set()
  for result in results['matches']:
    ids.add(result['id'])
  return ids

def get_all_ids_from_index():
  num_vectors = index.describe_index_stats()["namespaces"][""]['vector_count']
  all_ids = set()
  while len(all_ids) < num_vectors:
    input_vector = np.random.rand(1536).tolist()
    ids = get_ids_from_query(index,input_vector)
    all_ids.update(ids)

  return all_ids

def upsert_embeddings_to_pinecone(embeddings, name):
    vectors = []
    for embedding in embeddings:
       print(embedding)
       vectors.append({
            "id": name,
            "values": embedding["embedding"],
            "metadata": {
                "text": embedding["text"]
            }
        })
    index.upsert(vectors)
    files = get_all_ids_from_index()
    files.add(name)
    return files 

def deleteNamespace(id):
    index.delete(ids=[id], namespace="") 