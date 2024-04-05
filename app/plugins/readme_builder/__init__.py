import os
import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.commands import Command
import re

from .utils import Utils
from .repo_retrieval import RepoRetrieval

utl = Utils() # for utility functions
rr = RepoRetrieval() # for github retrieval

class ReadMeChat(Command):
    def __init__(self):
        super().__init__()
        self.history = []
        self.name = "readme"
        self.description = "Generate a custom readme."

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
        logging.info(f"OpenAI API call made. Tokens used: {tokens_used}")
        return response, tokens_used
    
    # start terminal
    def execute(self, *args, **kwargs):
        character_name = kwargs.get("character_name", "Readme Builder")
        print(f"\nWelcome to the GitHub Readme Generator. Type 'help' for a list of commands.")

        # Retrieve repository contents based on the provided URL
        # repository_contents = self.get_repository_contents(repository_url, github_token)

        while True:
            user_input = input("readme >>> ").strip()
            self.history.append(("user", user_input))
            commands = user_input.split()

            # empty command
            if user_input == "" :
                continue
            
            # done command : exit the program
            elif user_input.lower() == "exit":
                rr.git.close
                print("Goodbye.\n\n")
                break
            
            # help command : list commands
            elif user_input.lower() == "help":
                print("\nHelp Commands:")
                print("exit : exit the program")
                print("url <repository_url> : search for a github repository")
                print("structure : collect the repository file structure")
                print("download : retrieve a github repository")
                print("download <file_name> <file_name> ... : retrieve specific files from a github repository")
                print("download <directory_location> : retrieve a folder from a  github repository")
                print("delete : clear the current downloaded files")
                print("\n")

            # send files to ai
            elif commands[0] == "ai" :
                user_code_input = utl.build_text_file()
                try:
                    response, tokens_used = self.interact_with_ai(user_code_input, character_name)
                    print(f"AI Agent: {response}")
                    print(f"(This interaction used {tokens_used} tokens.)")
                    self.history.append(("system", response))
                except Exception as e:
                    print("Sorry, there was an error processing your request. Please try again.")
                    logging.error(f"Error during interaction: {e}")

            # url : search for repository
            elif commands[0] == "url" and len(commands) == 2:
                match = re.search(r"github\.com/([^/]+)/([^/]+)", commands[1])
                if match:
                    # request repo connection
                    print(f"Searching github for {match.group(2)} ...")
                    rr.connect_to_repository(match.group(2), match.group(1))
                    # print repo size    
                    print(f"Repository size: {rr.convert_from_bytes(rr.repo.size)}")
                else:
                    print("Invalid repository url.")

            # download : retrieve repo contents
            elif commands[0] == "download":
                if rr.repo is None:
                    print("ERROR: Not connected to a repository. Use 'url' to connect to one.")

                elif rr.repo.size > rr.max_repo_size :            
                    print(f"ERROR: This repository exceeds the maximum download limit of {rr.convert_from_bytes(rr.max_repo_size)}.")
                    print(f"This repository is {rr.convert_from_bytes(rr.repo.size)}")
                    print(f"Use 'download <file_name> <file_name> ...' to select specific files.")
                    print(f"Use 'download <directory_location>' to select a specific directory.")
                    return False
                
                # download entire directory
                elif len(commands) == 1 :
                    rr.recursive_download(rr.repo.get_contents(""), rr.init_local_dir(True))

                elif len(commands) > 1 :
                        # download folder
                        if len(commands) == 2 and os.path.isdir(commands[1]) :
                            rr.recursive_download(rr.repo.get_contents(commands[1]), rr.init_local_dir(False))

                        # download specified files
                        else :
                            for cmd in commands[1:] :
                                try :
                                    rr.download_file(rr.repo.get_contents(cmd), rr.init_local_dir(False))
                                except :
                                    print(f"ERROR: Invalid path: {cmd}")

                print("Download complete.")

            # delete : clear the current downloaded files
            elif user_input == "delete" :
                rr.init_local_dir(True)
                print("Local repository cleared.")

            # structure : collect the repository file structure
            elif user_input == "structure" :
                rr.save_file_structure(rr.repo, os.path.join(rr.local_dir, "file_structure.json"))


            # unknown command
            else :
                print("ERROR: Unknown command. Use 'help' for a list of commands.")

            '''
            try:
                response, tokens_used = self.interact_with_ai(user_input, character_name)
                print(f"AI Agent: {response}")
                print(f"(This interaction used {tokens_used} tokens.)")
                self.history.append(("system", response))
            except Exception as e:
                print("Sorry, there was an error processing your request. Please try again.")
                logging.error(f"Error during interaction: {e}")
                '''