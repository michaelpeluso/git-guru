import sys
from app.frontend import app as flask_app
from app.backend.utils.command_line import Backend
from app.backend.utils.get_api_limit import print_rates

if __name__ == "__main__":

    # show github rate limit
    print_rates()

    # run an instance of the backend in terminal
    if len(sys.argv) > 1 and sys.argv[1] == "backend" :
        Backend().execute()
        
    # Run the frontend app
    else:
        flask_app.run(debug=True)