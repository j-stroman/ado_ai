# Embedding model to use.
embedding_model_name_or_path = "models/all-MiniLM-L6-v2"

# Chromadb variables
chromadb_host = "localhost"
chromadb_port = 8000

# What to name the collection in Chromadb
vector_collection_name = "workitems"

# The raw CSV file from ADO
raw_csv_file_path = "data/workitems.csv"

# The sanitized and parsed CSV file
csv_file_path = "data/workitems_sanitized_parsed.csv"

# columns in the csv file containing metadata to be stored in vector db
csv_metadata_columns = ["ID", "Assigned To"]