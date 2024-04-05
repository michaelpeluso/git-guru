import os

class Utils :

    def read_files_from_directory(self, local_dir):
        files_content = []

        for root, dirs, files in os.walk(local_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    files_content.append((file_path, file_content))  # Append a tuple (file_path, file_content)
        return files_content
    
    def build_text_file(self):
        files_content = self.read_files_from_directory(os.getenv('LOCAL_REPO_DIRECTORY'))

        user_input = ""
        for file_path, file_content in files_content:
            # add divider before each file
            user_input += f"{'='*30}\nFile Location: {file_path}\n{'='*30}\n{file_content}\n\n"
        return user_input