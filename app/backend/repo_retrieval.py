from github import Github
from github import GithubException
import os
from dotenv import find_dotenv, load_dotenv
import requests
import shutil
import json

load_dotenv(find_dotenv())

class RepoRetrieval :
    def __init__(self):
        self.local_dir = os.getenv('LOCAL_REPO')
        self.git = None
        self.repo = None
        self.max_repo_size = 2 ** 27 # 128 megabytes

        try :
            self.git = Github(os.getenv('GITHUB_ACCESS_TOKEN'))
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
        if self.git == None :
            print("ERROR: Authentication required.")
            return

        try :
            # request connection
            self.repo = self.git.get_user(user).get_repo(repo_name)
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

    # download list of files
    def download_files_batch(self, files=None, preserve_structure=True):
        if files is None:
            # If no specific list of files is provided, download all files
            files = self.repo.get_contents("")

        try:
            # Batch download files recursively
            for file in files:
                if file.type == "dir":
                    if preserve_structure:
                        # Recursively download files in subdirectories
                        subdirectory_files = self.repo.get_contents(file.path)
                        self.download_files_batch(subdirectory_files, preserve_structure)
                        # Create directories if preserve_structure is True
                        os.makedirs(os.path.join(self.local_dir, file.path), exist_ok=True)
                else:
                    file_url = file.download_url
                    response = requests.get(file_url)
                    if preserve_structure:
                        # Create directories based on file path
                        file_path = os.path.join(self.local_dir, file.path)
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                    else:
                        with open(os.path.join(self.local_dir, file.name), 'wb') as f:
                            f.write(response.content)
                    print(f"Downloaded: {self.local_dir}/{file.name}")
        except Exception as e:
            print(f"ERROR: Could not download files: {e}")

    # save file structure as a json to file_structure.json
    def save_file_structure(self, repo, file_name):
        print("Collecting the repository file structure... This may take a moment...")
        try:
            def traverse_directory(directory, directory_structure):
                # Batch fetch directory contents
                contents = repo.get_contents(directory)
                contents_dict = {content.name: content for content in contents}

                for content in contents:

                    # directory
                    if content.type == "dir":
                        # Check if the directory contents are already cached
                        if content.name in directory_structure:
                            sub_directory_structure = directory_structure[content.name]["contents"]
                        else:
                            sub_directory_structure = {}
                            directory_structure[content.name] = {
                                "name": content.name,
                                "path": content.path,
                                "type": "directory",
                                "contents": sub_directory_structure
                            }
                            # Cache the directory contents
                            directory_structure[content.name]["contents"] = traverse_directory(content.path, sub_directory_structure)

                    # file
                    elif content.type == "file":
                        # Add file information directly to directory_structure
                        try:
                            decoded_content = content.decoded_content.decode('utf-8')
                        except UnicodeDecodeError:
                            decoded_content = "Unable to decode content (non-UTF-8 encoding)"
                        file_info = {
                            "name": content.name,
                            "type": "file",
                            "path": content.path,
                            "size": content.size,
                            "top_content": decoded_content.splitlines()[:3]
                        }
                        directory_structure[content.name] = file_info

                    # symbolic link
                    elif content.type == "symlink":
                        file_info = {
                            "name": content.name,
                            "type": "link",
                            "path": content.path,
                            "target": content.target
                        }
                        directory_structure[content.name] = file_info

                return directory_structure

            file_structure_json = traverse_directory("", {})
            
            # Save the file structure as JSON to a file
            with open(file_name, "w") as file:
                json.dump(file_structure_json, file, indent=4)
            print("File structure saved successfully.")
        except Exception as e:
            print(f"ERROR: There was an issue saving the file structure: {e}")
