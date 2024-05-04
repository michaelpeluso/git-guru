from flask import Flask, render_template, request, jsonify
import os
import json
from dotenv import find_dotenv, load_dotenv
from app.backend import Backend  

load_dotenv(find_dotenv())

# create Flask app
app = Flask(__name__)

# initialize the backend
backend = Backend()

# Route to handle command input and output
@app.route('/', methods=['GET', 'POST'])
def command_prompt():
    # just return index page
    return render_template('index.html')

# route to handle file selection
@app.route('/file-selection', methods=['GET', 'POST'])
def show_files():

    # get repo link
    url_cmd = "url " + request.form['repo_url']
    cmd_output = backend.execute(user_input=url_cmd)
    cmd_output = backend.execute(user_input="structure")
    print(cmd_output)

    # get file content
    LOCAL_REPO = os.getenv('LOCAL_REPO')
    json_file_path = os.path.join(LOCAL_REPO, "file_structure.json")

    with open(json_file_path, 'r') as file:
        json_data = json.dumps(json.load(file))

        if not json_data:
            return render_template('select-files.html', json_data={"message": "No data available"})

    # return page and data
    return render_template('select-files.html', json_data=json_data)

# run
if __name__ == '__main__':
    app.run(debug=True)
