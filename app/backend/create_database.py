import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import shutil
from dotenv import find_dotenv, load_dotenv
from app.backend.utils.log_manager import log_api_usage

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LOCAL_REPO = os.getenv('LOCAL_REPO')
CHROMA_PATH = os.getenv('CHROMA_PATH')

def generate_database(chunk_size=750, chunk_overlap=75):
    init_dir()
    documents = load_documents()
    
    chunks = split_text(documents, chunk_size, chunk_overlap)
    save_to_chroma(chunks, chunk_size)
    add_log(chunks, chunk_size)

def load_documents():
    documents = []
    for root, dirs, files in os.walk(LOCAL_REPO):
        for file in files:
            file_path = os.path.join(root, file)
            # Process the file and create a Document object
            # For simplicity, let's assume you have a function to create a Document from a file path
            document = create_document(file_path)
            documents.append(document)
    return documents

def create_document(file_path):
    # This is where you process the file and create a Document object
    # You need to implement this based on your file structure and data extraction logic
    # For simplicity, let's assume you have a function to extract text from a file
    try :
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except Exception as e :
        error = f"Error reading file '{file_path}': {e.__class__.__name__}. Skipping this file."
        print(error)
        document = Document(page_content=error, metadata={"source": file_path})
        return document

    # Create the Document object with the extracted file content and metadata
    document = Document(page_content=file_content, metadata={"source": file_path})
    return document

def split_text(documents: list[Document], chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    if len(chunks) > 0:
        document = chunks[0]
        print(document.page_content)
        print(document.metadata)

    return chunks

def save_to_chroma(chunks: list[Document], chunk_size):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    
    db = Chroma.from_documents(chunks, model, persist_directory=CHROMA_PATH)

    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

# initialize chroma directory 
def init_dir(clear_dir=True):

    # Check if the directory exists
    if os.path.exists(CHROMA_PATH):
        
        # delete contents
        if clear_dir:
            for root, dirs, files in os.walk(CHROMA_PATH):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
            
            print(f"Cleared contents of {CHROMA_PATH}.")
        
        else:
            print(f"Directory {CHROMA_PATH} already exists. Contents not cleared.")
    
    # create directory
    else:
        os.makedirs(CHROMA_PATH)
        os.chmod(CHROMA_PATH, 0o777)
        print(f"Created directory {CHROMA_PATH}.")
    
    # Check directory permissions
    if not os.access(CHROMA_PATH, os.W_OK):
        print(f"Error: Insufficient permissions to access or write to directory '{CHROMA_PATH}'.")

def add_log(chunks, chunk_size) :
    # $0.0001 to $0.00002 / 1k tokens  
    price_per_token = 0.00000006
    total_tokens = chunk_size * len(chunks)
    total_cost = price_per_token * total_tokens
    log_api_usage("Embedding", total_tokens, 0, total_cost)