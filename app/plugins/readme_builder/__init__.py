import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.commands import Command

from github import Github
from github import GithubException
import re
import requests
import shutil


class ReadMeChat(Command):
    def __init__(self):
        super().__init__()
        self.name = "readme"
        self.description = "Generate a custom readme."
        self.git = None
        self.history = []
        self.files = []
        self.repo = None
        self.curr_repo_size = 0
        self.max_repo_size = 2 ** 10 # 1 megabyte

        load_dotenv()

        # connect to GitHub
        try :
            self.git = Github(os.getenv('GITHUB_ACCESS_TOKEN'))
        except Exception or GithubException as e :
            print(f"ERROR: Unable to connect to GitHub. Type 'exit' to return home.")

        API_KEY = os.getenv('OPEN_AI_KEY')
        self.llm = ChatOpenAI(openai_api_key=API_KEY, model="gpt-3.5-turbo")  # This is default 3.5 chatGPT
        # chatGPT 4: "gpt-4-0125-preview"
        
    def calculate_tokens(self, text):
        # More accurate token calculation mimicking OpenAI's approach
        return len(text) + text.count(' ')

    def interact_with_ai(self, user_input, character_name):
        # Generate a more conversational and focused prompt
        prompt_text = "Your main goal is to help the client build a README.md file. They can either describe their code in english, or paste their entire codebase. You will read this code, interpret its goal, and construct a satisfactory README.md file."
        prompt = ChatPromptTemplate.from_messages(self.history + [("system", prompt_text)])
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": user_input})

        # Token usage logging and adjustment for more accurate counting
        tokens_used = self.calculate_tokens(prompt_text + user_input + response)
        logging.info(f"OpenAI API call made. Tokens used: {tokens_used}")
        return response, tokens_used
    
    def execute(self, *args, **kwargs):
        character_name = kwargs.get("character_name", "Movie Expert")
        print(f"\nWelcome to the GitHub Readme Generator. Type 'help' for a list of commands.")

        # Retrieve repository contents based on the provided URL
        # repository_contents = self.get_repository_contents(repository_url, github_token)

        while True:
            user_input = input("readme >>> ").strip()
            commands = user_input.split()

            # empty command
            if user_input == "" :
                continue
            
            # done command : exit the program
            elif user_input.lower() == "exit":
                self.git.close
                print("Goodbye.\n\n")
                break
            
            # help command : list commands
            elif user_input.lower() == "help":
                print("\nHelp Commands:")
                print("exit : exit the program")
                print("url <repository_url> : search for a github repository")
                print("\n")
                continue

            # url : search for repository
            elif commands[0] == "url" and len(commands) == 2:
                match = re.search(r"github\.com/([^/]+)/([^/]+)", commands[1])
                if match:
                    print(f"Searching github for {match.group(2)} ...")
                    self.connect_to_repository(match.group(2), match.group(1))
                else:
                    print("Invalid repository url.")
                continue

            # download : save repository
            elif user_input == "download" :
                self.download_repository()

            # unknown command
            else :
                print("ERROR: Unknown command. Use 'help' for a list of commands.")

            self.history.append(("user", user_input))
            
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

    def connect_to_repository(self, repo_name, user):
        if self.git == None :
            print("ERROR: Authentication required.")
            return

        try :
            self.repo = self.git.get_user(user).get_repo(repo_name)
            print(f"Successfully connected to {repo_name}")
            
            size_in_bytes = self.repo.size
            
            # Determine the most reasonable unit
            units = ['bytes', 'KB', 'MB', 'GB', 'TB']
            unit_index = 0
            while size_in_bytes >= 1024 and unit_index < len(units) - 1:
                size_in_bytes /= 1024
                unit_index += 1

            print(f"repo size: {size_in_bytes:.3f} {units[unit_index]}")

        except Exception or GithubException as e:
            print(f"Error: Unable to access repository.")

    # access files from github
    def download_repository(self):
        if self.repo == None :
            print("ERROR: Not connected to a repository. Use 'url' to connect to one.")
            return False
        
        if self.repo.size > self.max_repo_size :
            print(f"ERROR: This repository exceeds the maximum download limit of 100 Megabytes ({self.repo.size}/{self.max_repo_size}).")
            print(f"Use 'download <filename/directory> <filename/directory> ...' to select specific files.")
            return False
        
        # Clear local directory or create one if it doesn't exist
        local_dir = "./local_repo"
        if os.path.exists(local_dir) :
            shutil.rmtree(local_dir)
        os.makedirs(local_dir, exist_ok=True)

        # Download files recursively
        if not self.recursive_download(self.repo.get_contents(""), local_dir) :
            return False # terminate recursion
        return True

    # walk through directories
    def recursive_download(self, contents, local_dir) :
        file_count = 0
        total_files = len(contents)
        for file in contents:
            try:
                # directory
                if file.type == "dir" :
                    self.recursive_download(self.repo.get_contents(file.path), local_dir)
                else :
                    # check if files exceed 100 Mbs
                    file_size = int(file.size)
                    if self.curr_repo_size + file_size > self.max_repo_size :
                        print(f"ERROR: Download limit exceeded: {self.max_repo_size} bytes.")
                        self.curr_repo_size += file_size
                        return

                    # download file
                    try :
                        file_url = file.download_url
                        response = requests.get(file_url)
                        with open(os.path.join(local_dir, file.name), 'wb') as f :
                            f.write(response.content)
                            self.curr_repo_size += int(file.size)
                    except Exception or GithubException as e :
                        print(f"ERROR: Could not download content {os.path.relpath(__file__, './local_repo')}")

            except Exception as e:
                print(f"ERROR: Could not find repository directory {os.path.relpath(__file__, './local_repo')}")
    
            # increment file count
            file_count += 1
            print(f"Downloaded {file_count}/{total_files}")

    # send message to openai
    def interact_with_ai(self, user_input, character_name):
        prompt_text = "Your main goal is to help the client build a README.md file. They can either describe their code in English or paste their entire codebase. You will read this code, interpret its goal, and construct a satisfactory README.md file."
        prompt = ChatPromptTemplate.from_messages(self.history + [("system", prompt_text)])
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": user_input})

        tokens_used = self.calculate_tokens(prompt_text + user_input + response)
        logging.info(f"OpenAI API call made. Tokens used: {tokens_used}")
        return response, tokens_used