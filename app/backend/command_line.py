import os
import logging
import re
from json import dumps as jsonDumps
from app.backend.utils.file_manager import Filer
from app.backend.utils.ai_interactions import AI_Interactions
from app.backend.repo_retrieval import RepoRetrieval
from app.backend.create_database import generate_database
from app.backend.ai_interactions import query_ai

filer = Filer() # for utility functions
aii = AI_Interactions()
rr = RepoRetrieval() # for github retrieval

class Backend():
    def __init__(self):
        super().__init__()
        self.history = []
        self.name = "readme"
        self.description = "Generate a custom readme."
        
    # start terminal
    def execute(self, *args, **kwargs):
        if (len(self.history) == 0) :
            self.print_to_user(f"\nWelcome to the GitHub Readme Generator. Type 'help' for a list of commands.")

        # Retrieve repository contents based on the provided URL
        # repository_contents = self.get_repository_contents(repository_url, github_token)

        while True:
            user_input = input("readme >>> ").strip()
            self.history.append(("user", user_input))
            commands = user_input.split()

            # empty command
            if user_input == "" :
                self.print_to_user("")
            
            # done command : exit the program
            elif user_input.lower() == "exit":
                rr.git.close
                self.print_to_user("Goodbye.\n\n")
                return  
            
            # help command : list commands
            elif user_input.lower() == "help":
                self.print_to_user("\nHelp Commands:"
                    "\nexit : exit the program"
                    "\nurl <repository_url> : search for a github repository"
                    "\nstructure : collect the repository file structure"
                    "\ndownload : retrieve a github repository"
                    "\ndownload <file_name> <file_name> ... : retrieve specific files from a github repository"
                    "\ndatabase : cluster and store data in a data structure"
                    "\nquery <query_string> : query open ai about the data"
                    "\ndelete : clear the current downloaded files"
                    "\n")
    
            # url : search for repository
            elif commands[0] == "url" and len(commands) == 2:
                match = re.search(r"github\.com/([^/]+)/([^/]+)", commands[1])
                if match:
                    # request repo connection
                    self.print_to_user(f"Searching github for {match.group(2)} ...")
                    rr.connect_to_repository(match.group(2), match.group(1))
                    # print repo size
                    self.print_to_user(f"Repository size: {rr.convert_from_bytes(rr.repo.size * 1024)}")
                else:
                    self.print_to_user("Invalid repository url.")

            # download : retrieve repo contents
            elif commands[0] == "download":
                if rr.repo is None:
                    self.print_to_user("ERROR: Not connected to a repository. Use 'url' to connect to one.")

                elif rr.repo.size * 1024 > rr.max_repo_size :            
                    self.print_to_user(f"ERROR: This repository exceeds the maximum download limit of {rr.convert_from_bytes(rr.max_repo_size)}."
                        "\nThis repository is {rr.convert_from_bytes(rr.repo.size * 1024)}"
                        "\nUse 'download <file_name> <file_name> ...' to select specific files.")
                
                # download entire directory
                elif len(commands) == 1 :
                    try :
                        rr.download_files_batch()
                    except Exception as e :
                        self.print_to_user(f"ERROR: Unable to download entire repository: {e}")

                # download specified files
                elif len(commands) > 1 :
                    try :
                        specified_files = commands[1:]
                        rr.download_files_batch(specified_files)
                        self.print_to_user("Download complete.")
                    except Exception as e:
                        self.print_to_user(f"ERROR: Unable to download {specified_files}: {e}")

            # delete : clear the current downloaded files
            elif user_input == "delete" :
                rr.init_local_dir(True)
                self.print_to_user("Local repository cleared.")

            # structure : collect the repository file structure
            elif user_input == "structure" :
                rr.retrieve_file_structure()
                self.print_to_user("Saved file structure.")
            
            # database : cluster and store data in a data structure
            elif commands[0] == "database":
                self.print_to_user("Generating database...")
                generate_database()
                self.print_to_user("Generated database.")
        
            # query : query open ai about the data
            elif commands[0] == "query":
                # stitch together command
                joined_commands = " ".join(commands)
                commands = joined_commands.split(maxsplit=1)

                # check for valid query
                if (len(commands) != 2) :
                    self.print_to_user("Must input a query as an argument.")
                    
                self.print_to_user("Querying ai with prompt...")
                prompt = commands[1]
                response = query_ai(prompt)
                response = jsonDumps(response)
                
                if (response == {}) :
                    self.print_to_user("No data returned.")
                
                self.print_to_user(response)

            # unknown command
            else :
                self.print_to_user("ERROR: Unknown command. Use 'help' for a list of commands.")

    # print and save to history
    def print_to_user(self, input):
        self.history.append(("system", input))
        print(input)
        return input
            
if __name__ == "__main__":
    app = Backend()
    app.execute()
