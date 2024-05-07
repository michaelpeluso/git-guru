from github import Github
from github import GithubException
import os
from dotenv import find_dotenv, load_dotenv
from app.backend.utils.get_api_limit import print_rates, is_limit_hit
import requests
import shutil
import json

load_dotenv(find_dotenv())

class RepoRetrieval :
    def __init__(self):
        self.local_dir = os.getenv('LOCAL_REPO')
        self.git = None
        self.repo = None
        self.user = None
        self.max_repo_size = 2 ** 27 # 128 megabytes

        try :
            self.git = Github(os.getenv('GITHUB_TOKEN'))

            # check if access token is valid
            if (self.git.get_rate_limit().core.limit == 60) :
                print("ERROR: GitHub personal access token is invalid")
                    
        except Exception or GithubException as e :
            print(f"ERROR: Unable to connect to GitHub: {e}")

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
        self.gh_api_limit()

        if self.git == None :
            print("ERROR: Authentication required.")
            return

        try :
            # request connection
            self.user = user
            self.repo = self.git.get_repo(f"{user}/{repo_name}")
            print(f"Successfully connected to {repo_name}")

        except Exception or GithubException as e:
            print(f"Error: Unable to access repository: {e}")

    # Clear local directory or create one if it doesn't exist
    def init_local_dir(self, clear_dir):
        local_dir = self.local_dir
        if os.path.exists(local_dir) and clear_dir :
            shutil.rmtree(local_dir)
        os.makedirs(local_dir, exist_ok=True)
        return local_dir
    
    # check if api rate limit is reached
    def gh_api_limit(self) :
        if (is_limit_hit()) :
            print_rates()
            return True
        return False

    def download_files_batch(self, files=None):
        if files is None:
            files = []

        # Ensure self.repo is initialized
        if self.repo is None:
            print("ERROR: Repository not initialized.")
            return

        try:
            # download entire repository if files provided
            if not files:
                files = self.repo.get_contents("")

            for file_path in files:
                file = self.repo.get_contents(file_path)
                if file.type == "dir":
                    subdirectory_files = self.repo.get_contents(file_path)
                    self.download_files_batch(subdirectory_files, preserve_structure=True)
                else:
                    file_url = file.download_url
                    response = requests.get(file_url)
                    print(file_url)
                    print(response)
                    file_path = os.path.join(self.local_dir, file.path)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {self.local_dir}/{file.name}")

        except Exception as e:
            print(f"ERROR: Could not download files: {e}")

    # save file structure as a json to file_structure.json
    def retrieve_file_structure(self, file_name="file_structure.json"):
        try:
            # get default branch github api sha
            branch = self.repo.get_branch(self.repo.default_branch)

            # get File Structure
            file_structure = self.repo.get_git_tree(branch.commit.sha, recursive=True)
        
            # Format file structure as desired
            formatted_structure = {}
            
        except Exception as e:
            print(f"ERROR: There was an accessing repository: {e}")
        
        try:

            # add meta information
            formatted_structure["meta"] = {
                "name" : "meta",
                "description" : "This JSON object represents a complete file structure of the codebase. (├─│└)"
            }

            # iterate through all contents
            for item in file_structure.tree:
                path_components = item.path.split('/')
                current_level = formatted_structure

                # iterate through each directories
                for component in path_components[:-1]:
                    if component not in current_level:
                        current_level[component] = {
                            "name": component,
                            "path": '/'.join(path_components[:path_components.index(component) + 1]),
                            "type": "directory",
                            "contents": {}
                        }
                    current_level = current_level[component]["contents"]
                # create file entry
                if item.type == "blob":
                    current_level[path_components[-1]] = {
                        "name": path_components[-1],
                        "type": "file",
                        "path": item.path,
                        "size": item.size
                    }
            
        except Exception as e:
            print(f"ERROR: There was an issue iterating through the file structure: {e}")
        
        try: 

            # save structure as json
            full_name = os.path.join(self.local_dir, "file_structure.json")
            
            with open(full_name, "w") as file :
                json.dump(formatted_structure, file, indent=4)

            print("File structure saved successfully.")

        except Exception as e:
            print(f"ERROR: There was an issue saving the file structure: {e}")