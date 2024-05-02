from flask import Flask, render_template, request, jsonify
from app.backend import Backend  

app = Flask(__name__)

backend = Backend()

# Route to handle command input and output
@app.route('/', methods=['GET', 'POST'])
def command_prompt():
    if request.method == 'POST':
        if request.form['form'] == "url" :
            url_cmd = "url " + request.form['url_input']
            cmd_output = backend.execute(user_input=url_cmd)
            return jsonify({'message': cmd_output})
        else :
            return jsonify({'message': "cmd_output"})
    return render_template('index.html')
        

if __name__ == '__main__':
    app.run(debug=True)
