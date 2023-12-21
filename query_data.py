import sys

import chromadb
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

from constants import embedding_model_name_or_path, vector_collection_name, chromadb_host, chromadb_port

#----------------------------- Data Retrieval From ChromaDb -----------------------------#
'''
Connect to ChromaDB running in Docker
'''
chroma_client = chromadb.HttpClient(host=chromadb_host, port=chromadb_port)


'''
Create a transformer function using local LLM:
Create a new embedding function compatible with LangChain Chroma component
The SentenceTransformerEmbeddings class is an alias of the HuggingFaceEmbeddings class
It creates a sentence_transformers.SentenceTransformer instance using the 
specified model and adds the following methods:
  embed_documents(self, texts: List[str]) -> List[List[float]]
  embed_query(self, text: str) -> List[float]
'''
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
langchain_embedder = SentenceTransformerEmbeddings(
   model_name = embedding_model_name_or_path,
   model_kwargs = model_kwargs,
   encode_kwargs = encode_kwargs
)

'''
Tell LangChain to use Chromadb client and collection
Create a LangChain Chroma component and pass in the ChromaDb client, collection name,
and the compatible embedding function (instance of HuggingFaceEmbeddings)
'''
vector_store = Chroma(
    client = chroma_client, 
    collection_name = vector_collection_name,
    embedding_function = langchain_embedder
)

'''
Test the query
'''
query = "Create a new drop down menu for SDS app"
if len(sys.argv) > 1:
  query = sys.argv[1]

results = vector_store.similarity_search_with_relevance_scores(query)

for result in results:
    print("\n-------------------------------\n")
    print(result)
    
print("\n-------------------------------\n")