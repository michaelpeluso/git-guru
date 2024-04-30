from flask import Flask, render_template, request, jsonify
from app.backend import Backend  

app = Flask(__name__)

# Route to handle command input and output
@app.route('/', methods=['GET', 'POST'])
def command_prompt():
    if request.method == 'POST':
        user_input = request.form['user_input']  # Get the user input from the form
        Backend().start(user_input=user_input)  # Pass the user input to the backend
        return jsonify({'message': 'Command executed successfully.'})
    else:
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
