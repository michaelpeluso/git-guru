import os
from langchain.document_loaders import DirectoryLoader

DATA_PATH = os.getenv('LOCAL_REPO_DIRECTORY')

def load_documents() :
    loader = DirectoryLoader(DATA_PATH, glob="*")
    documents = loader.load()
    return documents

text_splitter = RecuresiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 500,
    length_function = len,
    add_start_index = True,
)

chunks = text_splitter.split_documents(documents)