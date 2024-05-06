from flask import Flask, render_template, request, jsonify
import os
import json
from dotenv import find_dotenv, load_dotenv
from app.backend import Backend  
from app.backend.utils.get_api_limit import print_rates, is_limit_hit

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
        #cmd_output = backend.execute(user_input=file_cmd)
        #print (cmd_output)

        return render_template('query.html')
    
    return render_template('query.html')


# run
if __name__ == '__main__':
    app.run(debug=True)
