import sys

import chromadb
from chromadb.utils import embedding_functions
from langchain.document_loaders.csv_loader import CSVLoader

'''
Process for loading ChromaDB with embeddings for our dataset and then querying the dataset

Loading Process:

  1. Split text into sentences while preserving metadata
    - First try using CSV Loader

  2. For each sentence, generate an embedding using the model we've downloaded locally

  3. Store the embedding in ChromaDb along with reference to its metadata

for example:
|-------------------------------------|---------------|
|              Metadata               |   Embedding   |
|-------------------------------------|---------------|
| Ticket ID, Assignee, Split Sentence |   [numbers]   |


Retrieval Process:

  4. Enter a description of a support ticket

  5. The description gets turned into and embedding using the chromadb model

  6. Chromadb runs a similiarity check of the items in the db

  7. Pulls top 5 results by similarity

  8. Parse the metadata and return the best determined assignee
'''

# Connect to ChromaDB running in Docker
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection_name = "workitems"
csv_file_path = "input.csv"
model_name = "models/all-MiniLM-L6-v2"

if len(sys.argv) > 1:
    csv_file_path = sys.argv[1]

# Load CSV data
loader = CSVLoader(
    file_path=csv_file_path,
    encoding="utf-8",
    metadata_columns=["ID", "Assigned To"],
)

data = loader.load()

print(data)
'''
[
  Document(
    page_content='Parsed: Parsed', 
    metadata={
      'source': 'ado_workitems_sanitized_clean.csv', 
      'row': 0, 
      'ID': 'ID', 
      'AssignedTo': 'AssignedTo'
    }
  ), ...
] 
'''

'''
Create a new embedding function compatible with ChromaDb collection:
The embedding_functions.SentenceTransformerEmbeddingsFunction class 
creates a sentence_transformers.SentenceTransformer instance using the
specified model and adds the following method:
  __call__(self, input: Documents) -> Embeddings
'''
chroma_embedder = embedding_functions.SentenceTransformerEmbeddingFunction(model_name)

# Reset collection
chroma_client.delete_collection(collection_name)

# Get or create chroma collection using the specified embedding function (instead of downloading their default)
collection = chroma_client.get_or_create_collection(name=collection_name, embedding_function=chroma_embedder)

# Add documents to the collection
for doc in data:
    collection.add(
        ids = [str(doc.metadata["ID"])],
        metadatas = doc.metadata,
        documents = doc.page_content
    )
