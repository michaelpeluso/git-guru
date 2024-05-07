from flask import Flask, render_template, request, jsonify
import os
import json
from dotenv import find_dotenv, load_dotenv
from app.backend import Backend 

load_dotenv(find_dotenv())
LOCAL_REPO = os.getenv('LOCAL_REPO')

# create Flask app
app = Flask(__name__, template_folder='html')

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

    if request.method == 'POST':

        # check request data
        if 'repo_url' not in request.form: 
            print("Request does not contain 'repo_url'")
            render_template('select-files.html')

        # if local_repo is empty
        cmd_output = ""
        
        # get repo link (1 request)
        url_cmd = "url " + request.form['repo_url']
        cmd_output += backend.execute(user_input=url_cmd)
        
        # delete local_repo contents (1 request)
        cmd_output += backend.execute(user_input="delete")
        
        # get structure (3 request)
        cmd_output += backend.execute(user_input="structure")

        print(cmd_output)

        # get file content
        json_file_path = os.path.join(LOCAL_REPO, "file_structure.json")

        with open(json_file_path, 'r') as file:
            json_data = json.dumps(json.load(file))

            if not json_data:
                return render_template('select-files.html', json_data={"message": "No data available"})

        # return page and data
        return render_template('select-files.html', json_data=json_data)

    # Default GET method behavior (can be updated as needed)
    return render_template('select-files.html')

# route to handle querying
@app.route('/query', methods=['GET', 'POST'])
def query_local_database():
    
    if request.method == 'POST':

        # check request data
        if ('files[]' not in request.form) :
            print("Request does not contain 'files'")
            return render_template('query.html')

        # get file array
        files = request.form.getlist('files[]')
        file_cmd = 'download'

        # create string of files
        if (len(files) > 0) : 
            file_string = ' '.join(files)
            file_cmd += ' ' + file_string

            print("Downloading " + str(len(files)) + " files/directories...")
            print(file_string)
            print("This may take a while...")

        else :
            print("Downloading all files...")

        # download content
        cmd_output = backend.execute(user_input=file_cmd)
        print (cmd_output)

        # saving content to database
        print("Saving files to database...")
        cmd_output = backend.execute(user_input="database")
        print("Files saved to database")
        print (cmd_output)

    return render_template('query.html')

# route to handle querying
@app.route('/ai', methods=['GET', 'POST'])
def ask_ai():

    if request.method == 'POST':

        # retrieve user query
        query = request.form.getlist('query_input')[0]

        # check request data
        if (not query) :
            print("Request does not contain 'query'")
            return jsonify({'response': "Request does not contain a query."})

        # execute the backend
        cmd_output = backend.execute(user_input="query '" + query + "'")
       
       # check for valid response
        try:
            data = json.loads(cmd_output)
        except json.JSONDecodeError:
            return jsonify({'response': 'Invalid JSON response from backend'})
        
        print(data)
        
        return jsonify(data)
    
    return jsonify({'error': "Not a POST request."})

# run
if __name__ == '__main__':
    app.run(debug=True)
