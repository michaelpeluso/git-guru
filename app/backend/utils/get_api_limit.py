import time
from github import Github

g = Github()
rate_limit = g.get_rate_limit()

def print_rates() :
    print()
    print("-------------------------------------------")
    print("GITHUB REQUEST STATUS")
    print("Total requests: ", rate_limit.core.limit)
    print("Remaining requests: ", rate_limit.core.remaining)
    print("Resets in : ", (int)((time.mktime(rate_limit.core.reset.timetuple()) - time.time()) // 60), "minutes left")
    print("-------------------------------------------")  
    print()