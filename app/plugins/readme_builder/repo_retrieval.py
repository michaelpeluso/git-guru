from github import Github
from github import GithubException
import os
import requests
import shutil
import json


class RepoRetrieval :
    def __init__(self):
        self.local_dir = os.getenv('LOCAL_REPO_DIRECTORY')
        self.git = None
        self.repo = None
        self.max_repo_size = 2 ** 30 # 1 gigabyte

        try :
            self.git = Github(os.getenv('GITHUB_ACCESS_TOKEN'))
        except Exception or GithubException as e :
            print(f"ERROR: Unable to connect to GitHub. Type 'exit' to return home.")

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