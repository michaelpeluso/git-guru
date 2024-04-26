import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

class AI_Interactions :

    def __init__ (self) :
        API_KEY = os.getenv('OPEN_AI_KEY')
        self.llm = ChatOpenAI(openai_api_key=API_KEY, model="gpt-3.5-turbo")  # This is default 3.5 chatGPT
        # chatGPT 4: "gpt-4-0125-preview"

    def calculate_tokens(self, text):
        # More accurate token calculation mimicking OpenAI's approach
        return len(text) + text.count(' ')

    def interact_with_ai(self, user_input, character_name):

        # Generate a more conversational and focused prompt
        prompt_text = "Your main goal is to help the client build a README.md file. This readme file will describe a users github repository. For you first message, the user will send a long string of files that he or she has chosen from their codebase that they believe is most relevant code regarding their project. You will read this code, interpret its goal, and construct a satisfactory README.md file immediately following the users initial message. The users will paste their code below. \n\n"
        prompt = ChatPromptTemplate.from_messages(self.history + [("system", prompt_text)])
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": user_input})

        # Token usage logging and adjustment for more accurate counting
        tokens_used = self.calculate_tokens(prompt_text + user_input + response)
        return response, tokens_used