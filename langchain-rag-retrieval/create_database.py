import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import shutil
from dotenv import load_dotenv

curr_file = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(curr_file, "..", ".env")
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv('OPEN_AI_KEY')
DATA_PATH = os.getenv('LOCAL_REPO_DIRECTORY')
CHROMA_PATH = curr_file + "/chroma"

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    documents = []
    for root, dirs, files in os.walk(DATA_PATH):
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
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # Create the Document object with the extracted file content and metadata
    document = Document(page_content=file_content, metadata={"source": file_path})
    return document

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
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

if __name__ == "__main__":
    main()
