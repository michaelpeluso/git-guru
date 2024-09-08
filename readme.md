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

### Slicing
Slicing refers to the process of dividing code snippets into manageable segments. This allows the AI to analyze smaller blocks of code rather than overwhelming it with large chunks. By breaking down the input, the system can focus on understanding the functionality and purpose of each segment, leading to more accurate and relevant README generation.

### Embedding
Embedding is a technique used to convert code snippets into numerical representations that capture semantic meaning. This transformation allows the AI to understand the relationships between various pieces of code and their contexts. By embedding code snippets, the system can effectively gauge their relevance to the overall project, enhancing the quality of the generated documentation.

### Storing in the Database
The project makes use of a robust database system to store embedded representations of the code snippets. This storage allows for quick retrieval and analysis of previously processed snippets, enabling the AI to draw from a wealth of information when generating documentation. The database is designed to maintain efficiency and speed, ensuring that the AI can operate without lag, even when processing extensive codebases.

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
.
├── .gitignore
├── .gitmodules
└── app
    ├── __init__.py
    └── backend
        ├── __init__.py
        ├── create_database.py
        ├── repo_retrieval.py
        └── utils
            ├── ai_interactions.py
            ├── file_manager.py
            ├── get_api_limit.py
            └── log_manager.py
    └── frontend
        └── static
            └── css
                ├── global.css
                ├── index.css
                ├── query.css
                └── select-files.css
            └── js
                ├── index.js
                ├── query.js
                └── select-files.js
        └── templates
            ├── index.html
            ├── query.html
            └── select-files.html
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
