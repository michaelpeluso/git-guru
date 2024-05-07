import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Define the logs directory path
LOGS_DIR = "./"
LOG_FILE = 'token_usage.txt'

def initialize_logs_directory():
    # Create the logs directory if it doesn't exist
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
        print(f"Created logs directory at {LOGS_DIR}")

    # Create the log file with a header if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as log_file:
            log_file.write("Total Cost: 0.0000000\n\n")
            log_file.write("Timestamp               Action         Tokens Input    Tokens Output    Cost\n")
            log_file.write("---------------------------------------------------------------------------------\n")
        print(f"Created log file at {LOG_FILE}")

def log_api_usage(action, tokens_input, tokens_output, cost):
    # Initialize the logs directory and log file
    initialize_logs_directory()

    # Generate the log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp:<23} {action:<15} {tokens_input:<15} {tokens_output:<15} {float(cost):.7f}\n"

    # Append the log entry to the log file
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_entry)

    # update total cost
    update_total_cost(LOG_FILE)

    print("API usage logged successfully.")

def update_total_cost(log_file):
    # Read the existing log file and calculate
    total_cost = 0.0
    log_lines = []
    with open(log_file, 'r') as file:
        for line in file:
            if "Total Cost" not in line:
                log_lines.append(line)
                parts = line.strip().split()
                if len(parts) == 6:
                    try:
                        cost = float(parts[-1])
                        total_cost += cost
                    # ignore invalid cost
                    except ValueError:
                        pass

    # add to the top of file
    with open(log_file, 'w') as file:
        file.write(f"Total Cost: {total_cost:.7f}\n")
        file.writelines(log_lines)

    print("Updated total cost in the log file.")