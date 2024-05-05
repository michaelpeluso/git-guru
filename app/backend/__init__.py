import os
import logging
import re

from app.backend.utils.file_manager import Filer
from app.backend.utils.ai_interactions import AI_Interactions
from app.backend.repo_retrieval import RepoRetrieval

filer = Filer() # for utility functions
aii = AI_Interactions()
rr = RepoRetrieval() # for github retrieval

class Backend():
    def __init__(self):
        super().__init__()
        self.history = []
        self.name = "readme"
        self.description = "Generate a custom readme."
        # rr.init_local_dir(True)
        
    # start terminal
    def execute(self, user_input):
        if (len(self.history) == 0) :
            self.print_to_user(f"\nWelcome to the GitHub Readme Generator. Type 'help' for a list of commands.")

        # Retrieve repository contents based on the provided URL
        # repository_contents = self.get_repository_contents(repository_url, github_token)

        user_input = user_input
        self.history.append(("user", user_input))
        commands = user_input.split()

        # empty command
        if user_input == "" :
            return self.print_to_user("")
        
        # done command : exit the program
        elif user_input.lower() == "exit":
            rr.git.close
            return self.print_to_user("Goodbye.\n\n")            
        
        # help command : list commands
        elif user_input.lower() == "help":
            return self.print_to_user("\nHelp Commands:"
                "\nexit : exit the program"
                "\nurl <repository_url> : search for a github repository"
                "\nstructure : collect the repository file structure"
                "\ndownload : retrieve a github repository"
                "\ndownload <file_name> <file_name> ... : retrieve specific files from a github repository"
                "\ndownload <directory_location> : retrieve a folder from a  github repository"
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
                return self.print_to_user(f"Repository size: {rr.convert_from_bytes(rr.repo.size * 1024)}")
            else:
                return self.print_to_user("Invalid repository url.")

        # download : retrieve repo contents
        elif commands[0] == "download":
            if rr.repo is None:
                self.print_to_user("ERROR: Not connected to a repository. Use 'url' to connect to one.")

            elif rr.repo.size * 1024 > rr.max_repo_size :            
                return self.print_to_user(f"ERROR: This repository exceeds the maximum download limit of {rr.convert_from_bytes(rr.max_repo_size)}."
                    "\nThis repository is {rr.convert_from_bytes(rr.repo.size * 1024)}"
                    "\nUse 'download <file_name> <file_name> ...' to select specific files.")
            
            # download entire directory
            elif len(commands) == 1 :
                try :
                    rr.download_files_batch()
                except Exception as e :
                    return self.print_to_user(f"ERROR: Unable to download entire repository: {e}")

            # download specified files
            elif len(commands) > 1 :
                try :
                    specified_files = commands[1:]
                    rr.download_files_batch(specified_files)
                    return self.print_to_user("Download complete.")
                except Exception as e:
                    return self.print_to_user(f"ERROR: Unable to download {specified_files}: {e}")

        # delete : clear the current downloaded files
        elif user_input == "delete" :
            rr.init_local_dir(True)
            return self.print_to_user("Local repository cleared.")

        # structure : collect the repository file structure
        elif user_input == "structure" :
            rr.retrieve_file_structure()
            return self.print_to_user("Saved file structure.")

        # unknown command
        else :
            return self.print_to_user("ERROR: Unknown command. Use 'help' for a list of commands.")

    # print and save to history
    def print_to_user(self, input):
        self.history.append(("system", input))
        print(input)
        return input
            
if __name__ == "__main__":
    app = Backend()
    app.execute()
