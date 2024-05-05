import os
from dotenv import find_dotenv, load_dotenv
import argparse
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import tiktoken


load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPEN_AI_MODEL = os.getenv('OPEN_AI_MODEL')
CHROMA_PATH = os.getenv("CHROMA_PATH")

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

--- End of context ---

Answer the question based on the above context: {question}
"""

# prompt_text = "Your main goal is to help the client build a README.md file. This readme file will describe a users github repository. The user will send a long string of files that he or she has chosen from their codebase that they believe is most relevant code regarding their project. You will read this code, interpret its goal, and construct a satisfactory README.md file. \n\n"

def main(total_snippets=10, relevance=0.25):
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
    results = db.similarity_search_with_relevance_scores(query_text, k=total_snippets)
    if len(results) == 0 or results[0][1] < relevance:
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

    # format response
    sources = [doc.metadata.get("source", None) for doc, _score in sorted_results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)

    # count tokens
    tokens_in = count_tokens(prompt)
    tokens_out = count_tokens(formatted_response)

    # calculate price
    price = calculate_price(tokens_in, tokens_out)

    # return collected data
    data = { 
            "tokens_in": tokens_in,
            "tokens_out": tokens_out, 
            "price": price, 
            "prompt": prompt,
            "response": formatted_response 
            }
    
    print(data)
    return data


def count_tokens(input: str):
    tokens = len(tiktoken.encoding_for_model(OPEN_AI_MODEL).encode(input))
    return tokens

def calculate_price(tokens_in, tokens_out) :
    price = None
    if (OPEN_AI_MODEL == "gpt-3.5-turbo") :
        price = tokens_in * 0.0000005 + tokens_in * 0.0000015

    elif (OPEN_AI_MODEL == "gpt-4") :
        price = tokens_in * 0.00003 + tokens_out * 0.00006
    
    price = "{:.7f}".format(price)
    return price

if __name__ == "__main__":
    main()
