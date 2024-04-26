import os
import logging
import re

from app.backend.utils.file_manager import Filer
from app.backend.repo_retrieval.repo_retrieval import RepoRetrieval

utl = Filer() # for utility functions
rr = RepoRetrieval() # for github retrieval

class Backend():
    def __init__(self):
        super().__init__()
        self.history = []
        self.name = "readme"
        self.description = "Generate a custom readme."
        
    # start terminal
    def start(self, *args, **kwargs):
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
                    response, tokens_used = Filer.interact_with_ai(user_code_input, character_name)
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
    app.start()
