# ADO Workitem Assignment

## Description
This project is a proof of concept for using embeddings to assign workitems to developers based on the similarity of the workitem description to the developer's previous workitems.

## Pre-requisites
- Python 3.10
- Docker
- Docker Compose

## Setup

After cloning the repository, follow these steps to setup the project:

2. **Create a Virtual Environment**  
   Open your terminal (or command prompt on Windows). Navigate to your project directory:
    ```bash
    cd /path/to/your/project
    ```
    Create a virtual environment:
    ```bash
    python3 -m venv env
    ```
3. **Activate the Virtual Environment**  
    Activate the virtual environment:
    ```bash
    source env/bin/activate
    ```
    On Windows:
    ```bash
    env/Scripts/activate
    ```
4. **Install the Dependencies**
    ```bash
    (env) > pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
    ```
    Make sure to include `--trusted-host pypi.org --trusted-host files.pythonhosted.org` at the end of the command if you are behind a proxy to avoid SSL errors.
5. **Download the Embedding Model**
    This step is necessary because the python library will try to download the model from the internet, which will fail due to SSL errors.  Instead, we will download the model manually from the HuggingFace and place it in the `./models` directory.
    Create a folder named `models` in the project root directory and navigate to it:
    ```powershell
    mkdir models
    cd models
    ```
    Clone the model from HuggingFace:
    ```powershell
    models > git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 
    ```
6. **Download, Build, and Run ChromaDb**
    This step is necessary because the pre-build docker image will run into errors when it tries
    to download the python packages from the internet.  Instead, we will download the source code
    and modify the `Dockerfile` to include the `--trusted-host pypi.org --trusted-host files.pythonhosted.org`
    flags to the `pip install` command and then build and run the docker image locally.
    ```powershell
    git clone https://github.com/chroma-core/chroma.git
    cd chroma
    chroma > docker-compose up -d --build
    ```
    Run the docker image:
    ```powershell
    chroma > docker run -p 8000:8000 chromadb/chroma
    ```

### Aqcuiring the dataset
The dataset for this project is the Azure DevOps work item history for the Azure DevOps project itself.
The dataset can be downloaded from the board view of the Azure DevOps project by going to the Queries tab
and creating a query to return all workitems with the field `'Assigned To' <> 'No one selected'` and 
`'Description' 'Is Not Empty'` to get a list of workitems that have been assigned to someone and have a
description. Click column options and make the following columns visible: `ID`, `Title`, `Assigned To`,
`Description`, `Tags`, and `State`. Click the `Export to CSV` button to download the dataset.

Example data:
| ID | Title | Assigned To | Description | Tags | State |
| --- | --- | --- | --- | --- | --- |
| 34536 | Edit dropdown menu options | User1 | "Add option for xyz in dropdown menu on dashboard" | Dashboard, UI | Done |

## Usage
1. **Fill in constants**
  Fill in the constants in the `constants.py` file with the appropriate values.
2. **Parse the dataset**  
  Parsing the data will combine the relevant columns into a single column and remove the unnecessary columns.
  This will create a file named `workitems_parsed.csv` in the same directory.
    ```bash
    (env) > python parser_data.py "data/workitems.csv"
    ```

    If this doesn't work, the data might need to be sanitized first. This can be done with the sanitize script:
    ```bash
    (env) > python sanitize_data.py "data/workitems.csv"
    ```
3. **Create the Embeddings**  
  Creating the embeddings will create a new column in the dataset with the embeddings for each workitem description and store them in chromadb along with its metadata (`ID` and `Assigned To`)
    ```bash
    (env) > python embed_data.py "data/workitems_parsed.csv"
    ```    
4. **Query the Embeddings**  
  Querying the embeddings will return the top 10 workitems that are most similar to the query workitem.
    ```bash
    (env) > python query_data.py "description of a ticket"
    ```
    This will print the top 4 workitems that are most similar to the provided description along with their similarity score.

## To Do

- [ ] Use ADO API to get workitems instead of using a CSV file

- [ ] Utilize PGVector to store embeddings instead of ChromaDB

- [ ] Determine whether text preprocessing/splitting is necessary and which library to use