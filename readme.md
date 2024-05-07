<sup><sub>This document was generated using only the resources within this repository.</sup></sub>

# GitGuru

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Requirements and Dependencies](#requirements-and-dependencies)
4. [Installation and Execution](#installation-and-execution-instructions)
5. [File Structure](#file-structure)
6. [Troubleshooting and FAQ](#troubleshooting-and-faq)

## Project Overview
This project is a GitHub README.md generator. It generates a comprehensive README.md file for your Github repository based on a set of provided code snippets. The generated README.md is designed to be comprehensive and long, filling more than a page.

## Features
- Automatic generation of README.md files based on provided code snippets
- Detection of syntax errors in the code snippets for improved clarity
- Querying functionality to extract relevant information from the codebase
- Provides a visual file structure tree using `file_structure.json`

### Requirements and Dependencies:
- Python 3.8
- Required Python packages specified in the `requirements.txt` file
- OpenAI API key (obtain from OpenAI platform)
- Local repository directory path for storing project files
- Chroma path for vectorstore operations
- Your Github repository URL

## Installation and Execution
0.**Quickstart**
- 1. Clone this repository to your local machine.
- 2. Navigate to the repository directory.
- 3. Install the required dependencies using `pip install -r requirements.txt`.
- 4. Run `python main.py` in your terminal.
1. **Start Python Virtual Environment:**
Open a terminal window. Navigate to the project directory. Create a new Python virtual environment by running the command:
```
python -m venv venv
```
Activate the virtual environment:
- On Windows:
```
venv\Scripts\activate
```
- On macOS and Linux:
```
source venv/bin/activate
```

2. **Install Requirements:**
3. Make sure you are in the virtual environment. Install the required dependencies from the `requirements.txt` file by running the command:
```
pip install -r requirements.txt
```

3. **Execute Commands:**
To run the application in on your browser, use the following command:
```
python main.py
```
To run the application in debug mode, use the following command:
```
python main.py debug
```
To run the backend functionality in the terminal, use:
```
python main.py backend
```

## Installation and Execution


## File Structure
```
.
├── .gitignore
├── .gitmodules
├── app
│ ├── __init__.py
│ ├── backend
│ │ ├── __init__.py
│ │ ├── create_database.py
│ │ ├── repo_retrieval.py
│ │ └── utils
│ │ ├── ai_interactions.py
│ │ └── file_manager.py
│ └── frontend
│ ├── static
│ │ ├── css
│ │ │ ├── global.css
│ │ │ └── index.css
│ │ │ ├── query.css
│ │ │ └── select-files.css
│ │ └── js
│ │ ├── index.js
│ │ ├── query.js
│ │ └── select-files.css
│ └── templates
│ └── index.html
│ └── query.html
│ └── select-files.html
├── README.md
├── __init__.py
├── main.py
├── package-lock.json
├── readme.md
└── requirements.txt
```

## Troubleshooting and FAQ
- If you encounter any issues during the installation process, please ensure you have the correct versions of Python and pip installed.
- If the README.md file is not generating as expected, ensure that your code snippets are relevant to your project.

---
Please note that this README.md file is generated and may not reflect the actual project's README.md file.
