import os
from datetime import datetime, timezone
from github import Github
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

g = Github(GITHUB_TOKEN)
rate_limit = g.get_rate_limit()

def print_rates() :
    print()
    print("-------------------------------------------")
    print("GITHUB REQUEST STATUS")
    print("Total requests: ", rate_limit.core.limit)
    print("Remaining requests: ", rate_limit.core.remaining)
    print("Resets in: ", round(((rate_limit.core.reset - datetime.now(timezone.utc)).total_seconds() / 60), 1), "minutes")
    print("-------------------------------------------")  
    print()

def is_limit_hit() :
    return rate_limit.core.limit == 0
