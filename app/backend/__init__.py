import os
import logging
import re

from app.backend.utils.file_manager import Filer
from app.backend.utils.ai_interactions import AI_Interactions
from app.backend.repo_retrieval.repo_retrieval import RepoRetrieval

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
    def execute(self, user_input):
        print(f"\nWelcome to the GitHub Readme Generator. Type 'help' for a list of commands.")

        # Retrieve repository contents based on the provided URL
        # repository_contents = self.get_repository_contents(repository_url, github_token)

        user_input = user_input
        self.history.append(("user", user_input))
        commands = user_input.split()

        # empty command
        if user_input == "" :
            return ""
        
        # done command : exit the program
        elif user_input.lower() == "exit":
            rr.git.close
            return("Goodbye.\n\n")            
        
        # help command : list commands
        elif user_input.lower() == "help":
            return("\nHelp Commands:"
            "\nexit : exit the program"
            "\nurl <repository_url> : search for a github repository"
            "\nstructure : collect the repository file structure"
            "\ndownload : retrieve a github repository"
            "\ndownload <file_name> <file_name> ... : retrieve specific files from a github repository"
            "\ndownload <directory_location> : retrieve a folder from a  github repository"
            "\ndelete : clear the current downloaded files"
            "\n")

        # send files to ai
        elif commands[0] == "ai" :
            user_code_input = filer.build_text_file()
            try:
                response, tokens_used = aii.interact_with_ai(user_code_input, character_name)
                return(f"AI Agent: {response}\n\n(This interaction used {tokens_used} tokens.)")
            except Exception as e:
                return("Sorry, there was an error processing your request. Please try again.")
                
        # url : search for repository
        elif commands[0] == "url" and len(commands) == 2:
            match = re.search(r"github\.com/([^/]+)/([^/]+)", commands[1])
            if match:
                # request repo connection
                print(f"Searching github for {match.group(2)} ...")
                rr.connect_to_repository(match.group(2), match.group(1))
                # print repo size
                return(f"Repository size: {rr.convert_from_bytes(rr.repo.size)}")
            else:
                return("Invalid repository url.")

        # download : retrieve repo contents
        elif commands[0] == "download":
            if rr.repo is None:
                print("ERROR: Not connected to a repository. Use 'url' to connect to one.")

            elif rr.repo.size > rr.max_repo_size :            
                return(f"ERROR: This repository exceeds the maximum download limit of {rr.convert_from_bytes(rr.max_repo_size)}."
                "\nThis repository is {rr.convert_from_bytes(rr.repo.size)}"
                "\n Use 'download <file_name> <file_name> ...' to select specific files."
                "\n Use 'download <directory_location>' to select a specific directory."
                )
            
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
                                return(f"ERROR: Invalid path: {cmd}")

            return("Download complete.")

        # delete : clear the current downloaded files
        elif user_input == "delete" :
            rr.init_local_dir(True)
            return("Local repository cleared.")

        # structure : collect the repository file structure
        elif user_input == "structure" :
            rr.save_file_structure(rr.repo, os.path.join(rr.local_dir, "file_structure.json"))
            return("Saved file structure.")

        # unknown command
        else :
            return("ERROR: Unknown command. Use 'help' for a list of commands.")

        '''
        try:
            response, tokens_used = Filer.interact_with_ai(user_input, character_name)
            print(f"AI Agent: {response}")
            print(f"(This interaction used {tokens_used} tokens.)")
            self.history.append(("system", response))
        except Exception as e:
            print("Sorry, there was an error processing your request. Please try again.")
            logging.error(f"Error during interaction: {e}")
            '''
            
if __name__ == "__main__":
    app = Backend()
    app.execute()
