import os

class Builder :
    def __init__(self) :
        self.local_dir = os.getenv('LOCAL_REPO_DIRECTORY')