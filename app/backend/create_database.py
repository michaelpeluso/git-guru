import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import shutil
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LOCAL_REPO = os.getenv('LOCAL_REPO')
CHROMA_PATH = os.getenv('CHROMA_PATH')

def generate_database():
    init_dir()
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

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

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
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

def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY), persist_directory=CHROMA_PATH
    )

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
        print(f"Created directory {CHROMA_PATH}.")