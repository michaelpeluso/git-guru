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
import json


class ReadMeChat(Command):
    def __init__(self):
        super().__init__()
        self.history = []
        self.name = "readme"
        self.description = "Generate a custom readme."
        self.local_dir = "./local_repo"
        self.git = None
        self.repo = None
        self.max_repo_size = 2 ** 30 # 1 gigabyte

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
    
    # start terminal
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
                print("structure : collect the repository file structure")
                print("download : retrieve a github repository")
                print("download <file_name> <file_name> ... : retrieve specific files from a github repository")
                print("download <directory_location> : retrieve a folder from a  github repository")
                print("delete : clear the current downloaded files")
                print("\n")
                continue

            # url : search for repository
            elif commands[0] == "url" and len(commands) == 2:
                match = re.search(r"github\.com/([^/]+)/([^/]+)", commands[1])
                if match:
                    # request repo connection
                    print(f"Searching github for {match.group(2)} ...")
                    self.connect_to_repository(match.group(2), match.group(1))
                    # print repo size    
                    print(f"Repository size: {self.convert_from_bytes(self.repo.size)}")
                else:
                    print("Invalid repository url.")
                continue

            # download : retrieve repo contents
            elif commands[0] == "download":
                if self.repo is None:
                    print("ERROR: Not connected to a repository. Use 'url' to connect to one.")
                    continue

                if self.repo.size > self.max_repo_size :            
                    print(f"ERROR: This repository exceeds the maximum download limit of {self.convert_from_bytes(self.max_repo_size)}.")
                    print(f"This repository is {self.convert_from_bytes(self.repo.size)}")
                    print(f"Use 'download <file_name> <file_name> ...' to select specific files.")
                    print(f"Use 'download <directory_location>' to select a specific directory.")
                    return False
                
                # download entire directory
                if len(commands) == 1 :
                    self.recursive_download(self.repo.get_contents(""), self.init_local_dir(True))

                elif len(commands) > 1 :
                        # download folder
                        if len(commands) == 2 and os.path.isdir(commands[1]) :
                            self.recursive_download(self.repo.get_contents(commands[1]), self.init_local_dir(False))

                        # download specified files
                        else :
                            for cmd in commands[1:] :
                                if not os.path.isfile(cmd) :
                                    print(f"ERROR: Invalid path: {cmd}")
                                    continue
                                self.download_file(self.repo.get_contents(cmd), self.init_local_dir(False))

                print("Download complete.")
                continue

            # delete : clear the current downloaded files
            elif user_input == "delete" :
                self.init_local_dir(True)
                print("Local repository cleared.")
                continue

            # structure : collect the repository file structure
            elif user_input == "structure" :
                self.save_file_structure(self.repo, os.path.join(self.local_dir, "file_structure.json"))
                continue


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
    
    # given a number of bytes, return a string given in the most reasonable unit 
    def convert_from_bytes(self, size_in_bytes):
        units = ['bytes', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = size_in_bytes

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.3f} {units[unit_index]}"

    # connect to git repository
    def connect_to_repository(self, repo_name, user):
        if self.git == None :
            print("ERROR: Authentication required.")
            return

        try :
            # request connection
            self.repo = self.git.get_user(user).get_repo(repo_name)
            print(f"Successfully connected to {repo_name}")

        except Exception or GithubException as e:
            print(f"Error: Unable to access repository.")

    # Clear local directory or create one if it doesn't exist
    def init_local_dir(self, clear_dir):
        local_dir = self.local_dir
        if os.path.exists(local_dir) and clear_dir :
            shutil.rmtree(local_dir)
        os.makedirs(local_dir, exist_ok=True)
        return local_dir

    # walk through directories
    def recursive_download(self, contents, local_dir) :
        for file in contents:
            try:
                # open directory and create one if it doesn't exist
                if file.type == "dir":
                    sub_dir = os.path.join(local_dir, file.name)
                    os.makedirs(sub_dir, exist_ok=True)
                    self.recursive_download(self.repo.get_contents(file.path), sub_dir)
                
                # download files
                else:
                    self.download_file(file, local_dir)

            except Exception or GithubException as e:
                print(f"ERROR: Could not download content {file.name}")

    # copy file from Guthub to local_repo
    def download_file(self, file, local_dir) :
        try:
            file_url = file.download_url
            response = requests.get(file_url)
            with open(os.path.join(local_dir, file.name), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {local_dir}/{file.name}")
        except : 
            print(f"ERROR: File not found: {local_dir}/{file.name}")
    
    # collect file structure and save in local_dir
    def save_file_structure(self, repo, file_name):
        print("Collecting the repository file structure... This may take a moment...")
        try:
            def traverse_directory(directory):
                contents = repo.get_contents(directory)
                directory_structure = {}
                for content in contents:
                    if content.type == "dir":
                        directory_structure[content.name] = traverse_directory(content.path)
                    elif content.type == "file":
                        directory_structure[content.name] = "file"
                return directory_structure

            file_structure_json = traverse_directory("")
            
            # Save the file structure as JSON to a file
            with open(file_name, "w") as file:
                json.dump(file_structure_json, file, indent=4)
            print("File structure saved successfully.")

        except :
            print(f"ERROR: Unable to collect file structure.")