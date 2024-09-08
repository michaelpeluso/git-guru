<sub><em>This document was generated using only the resources within this repository - minus the live demo.</sub></em>

# GitGuru

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Demo](#demo)
4. [Requirements and Dependencies](#requirements-and-dependencies)
5. [Installation and Execution](#installation-and-execution-instructions)
6. [File Structure](#file-structure)
7. [Logging System](#logging-system)
8. [Troubleshooting and FAQ](#troubleshooting-and-faq)

## Project Overview
The GitGuru project is designed to streamline the process of generating a custom README.md file for GitHub repositories. It leverages artificial intelligence to analyze code snippets and create a comprehensive README.md document.

## Features
- AI-Powered README Generation
- Error Detection
- Inquiry-Based Assistance

## Demo
https://github.com/michaelpeluso/git-guru/assets/94207078/d4856171-46a2-4868-8383-659f046b4f7c

### Requirements and Dependencies:
- Python 3.8
- Required Python packages specified in the `requirements.txt` file
- OpenAI API key (obtain from OpenAI platform)
- Chroma path for vectorstore operations
- Your Github repository URL

## Installation and Execution

0. **Quickstart**
- Clone this repository to your local machine.
-  Navigate to the repository directory.
-  Install the required dependencies using `pip install -r requirements.txt`.
-  Run `python main.py` in your terminal.
    
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

### Logging System

The logging system in this project is designed to track API usage and store relevant information in log files. The system initializes the logs directory and log file if they do not already exist. Each log entry includes a timestamp, action performed, tokens input, tokens output, and cost associated with the action. The log file is appended with each new log entry to maintain a history of API usage.

## File Structure
```
.
├── .gitignore
├── .gitmodules
└── app
│ ├── __init__.py
│ └── backend
│ │ ├── __init__.py
│ │ ├── create_database.py
│ │ ├── repo_retrieval.py
│ │ └── utils
│ │ │ ├── ai_interactions.py
│ │ │ ├── file_manager.py
│ │ │ ├── get_api_limit.py
│ │ └ └── log_manager.py
│ └── frontend
│ │ ├── static
│ │ │ └── css
│ │ │ │ ├── global.css
│ │ │ │ ├── index.css
│ │ │ │ ├── query.css
│ │ │ │ └── select-files.css
│ │ │ └── js
│ │ │ │ ├── index.js
│ │ │ │ ├── query.js
│ │ │ └ └── select-files.css
│ │ └── templates
│ │ │ ├── index.html
│ │ │ ├── query.html
│ └ └ └── select-files.html
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
