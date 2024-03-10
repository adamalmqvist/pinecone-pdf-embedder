from pinecone import Pinecone
import re
import openai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

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

# Define a function to preprocess text
def preprocess_text(text):
    # Replace consecutive spaces, newlines, and tabs
    text = re.sub(r'\s+', ' ', text)
    return text

def process_pdf(file_path):
    # create a loader
    loader = PyPDFLoader(file_path)
    # load your data
    data = loader.load()
    # Split your data up into smaller documents with Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    documents = text_splitter.split_documents(data)
    # Convert Document objects into strings
    texts = [str(doc) for doc in documents]
    return texts

# Define a function to create embeddings
def create_embeddings(texts):
   embeddings = []
   for text in texts:
        embedding = embeddings_model.embed_documents(text, chunk_size)[0]
        embeddings.append({
            "embedding": embedding,
            "text": text
        })
   return embeddings

# Define a function to upsert embeddings to Pinecone
def getUploadedFiles():
    stats = index.describe_index_stats()
    namespace_map = stats['namespaces']
    print(namespace_map)
    return namespace_map

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
    response = index.upsert(vectors)
    files = getUploadedFiles()
    files[name] = response["upserted_count"]
    return files 




def deleteNamespace(name):
    index.delete(delete_all=True, namespace=name) 