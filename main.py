# main.py
from app.backend import Backend    

# You must put this in your main.py because this forces the program to start when you run it from the command line.
if __name__ == "__main__":
    app = Backend().start()  # Instantiate an instance of App
