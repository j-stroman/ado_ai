import sys

import chromadb
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma


#----------------------------- Data Retrieval From ChromaDb -----------------------------#
# Connect to ChromaDB running in Docker
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
model_name = "models/all-MiniLM-L6-v2"
collection_name = "workitems"

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
   model_name = model_name,
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
    collection_name = collection_name,
    embedding_function = langchain_embedder
)

# test query
query = "Create a new drop down menu for SDS app"
if len(sys.argv) > 1:
  query = sys.argv[1]

results = vector_store.similarity_search_with_relevance_scores(query)

for result in results:
    print("\n-------------------------------\n")
    print(result)