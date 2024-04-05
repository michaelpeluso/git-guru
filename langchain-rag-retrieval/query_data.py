import os
from dotenv import load_dotenv
import argparse
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


curr_file = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(curr_file, "..", ".env")
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv('OPEN_AI_KEY')
OPEN_AI_MODEL = os.getenv('OPEN_AI_MODEL')
CHROMA_PATH = os.path.join(curr_file, "chroma")

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Check if the API key is loaded correctly
    if OPENAI_API_KEY is None:
        print("Error: OPEN_AI_KEY environment variable is not set.")
        return

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=10)
    if len(results) == 0 or results[0][1] < 0.25:
        print(f"Unable to find matching results.")
        return

    # Sort the results chronologically
    sorted_results = sorted(results, key=lambda x: x[0].metadata.get("timestamp", 0))

    # Construct the context text from sorted results
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in sorted_results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=OPEN_AI_MODEL)
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in sorted_results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
