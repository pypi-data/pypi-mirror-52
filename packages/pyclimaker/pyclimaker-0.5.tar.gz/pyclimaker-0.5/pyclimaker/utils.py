#define BLACK   "\033[30m"      /* Black */
#define RED     "\033[31m"      /* Red */
#define GREEN   "\033[32m"      /* Green */
#define YELLOW  "\033[33m"      /* Yellow */
#define BLUE    "\033[34m"      /* Blue */
#define MAGENTA "\033[35m"      /* Magenta */
#define CYAN    "\033[36m"      /* Cyan */
#define WHITE   "\033[37m" 

# Message prompting to user
def log_prompt(log_string):
    print(f"\033[1m>>> \033[34m{log_string}\033[0m", end=" ")

# Message indicating good process
def log_success(log_string):
    print(f"\033[32m{log_string}\033[0m")

# Message indicating warning
def log_warning(log_string):
    print(f"\033[33m{log_string}\033[0m")

# Message indicating failure
def log_failure(log_string):
    print(f"\033[31m{log_string}\033[0m")