# from .exceptions import InvalidBindingAttemptException
from .argprompts import PyCliArgPrompt
from . import utils

class PyCliMain():
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.MESSAGE_PROMPT_INVALID_COMMAND = "This is an invalid key"
        self.MESSAGE_EXIT = "Aborting the programme"
        self.functions = {}
        self.help_message_object = {}
    
    def bind_function(self, function_prompt, cli_command):
        if isinstance(function_prompt, PyCliFunctionPrompt) == False:
            raise Exception("Invalid attempt to bind an invalid function_prompt") 
        
        self.functions[cli_command] = function_prompt
        
        # Modify help message
        self.help_message_object[cli_command] = {}
        self.help_message_object[cli_command]["description"] = function_prompt.description


    def print_help_message(self):
        print(self.name + ":")
        print("".ljust(4), self.description)
        print()
        print("Command lists:")
        print("".ljust(4), "help".ljust(20), "Prints this message")
        print("".ljust(4), "exit".ljust(20), "Aborts the programme")

        for cli_command, function_prompt in self.functions.items():
            print("".ljust(4), cli_command.ljust(20), function_prompt.description)

            if len(function_prompt.arg_prompts) > 0:
                print("".ljust(4), "".ljust(20), "Options:")
                for arg_name, arg_prompt in function_prompt.arg_prompts.items():
                    print("".ljust(4), "".ljust(20), arg_name.ljust(24), arg_prompt.description)
                print()

    def run(self):
        print(f"Starging the programme")

        # Prompt-command-excution loop
        while True:
            utils.log_prompt(f"Enter function(alias) you want to execute:")
            command = input()
            
            if command in self.functions.keys():
                self.functions[command].trigger()
            elif command == "help":
                self.print_help_message()                
            elif command == "exit":
                print(self.MESSAGE_EXIT)
                break
            else:
                utils.log_warning(self.MESSAGE_PROMPT_INVALID_COMMAND)
            print()


class PyCliFunctionPrompt():
    def __init__(self, function, description):
        # Type checks
        if callable(function) == False:
            raise Exception("function must be a callable.")
        
        # Define helper variables
        if function.__defaults__ != None:
            argcount_non_defaults = function.__code__.co_argcount - len(function.__defaults__)
        else:
            argcount_non_defaults = function.__code__.co_argcount

        # Initialise attributes
        self.function = function
        self.description = description
        
        self.function_args = {} # Can be either defined by developers or inputted by users
        for i in range(function.__code__.co_argcount):
            if argcount_non_defaults < i:
                default_at_function = function.__defaults__[i]
            else:
                default_at_function = None
            
            self.function_args[function.__code__.co_varnames[i]] = {
                "is_changeable": True,
                "default_at_cli": None,
                "default_at_function": default_at_function
            }
        self.function_args_aliases = {key: key for key in self.function_args.keys()}
        
        # Properties to be filled by the developer
        self.arg_prompts = {}

    def bind_function_args_aliases(self, alias, arg_name):
        # Type checks
        if isinstance(alias, str) == False:
            raise TypeError("alias must be of type 'str'")

        if isinstance(arg_name, str) == False:
            raise TypeError("arg_name must be of type 'str'")

        # Runtime checks
        if arg_name not in self.function_args:
            raise Exception()

        self.function_args_aliases[alias] = arg_name

    def bind_default_cli_arg(self, arg_alias, arg_value, is_changeable):
        # Type checks
        if isinstance(arg_alias, str) == False:
            raise TypeError("arg_alias must be of type 'str'")

        if isinstance(is_changeable, bool) == False:
            raise Exception("is_changeable must be of type 'bool'")

        # Runtime checks
        if arg_alias not in self.function_args_aliases.keys():
            raise Exception("Invalid arg_name")
        
        arg_name = self.function_args_aliases[arg_alias]
        self.function_args[arg_name]["is_changeable"] = is_changeable
        self.function_args[arg_name]["default_at_cli"] = arg_value 
        
    def bind_arg_prompt(self, arg_prompt, arg_name_to_bind):
        # Type checks
        if isinstance(arg_prompt, PyCliArgPrompt) == False:
            raise TypeError("arg_prompt must be of type <class 'PyCliArgPrompt'>")
        
        if isinstance(arg_name_to_bind, str) == False:
            raise TypeError("arg_name_to_bind must be of type 'str'")

        # Runtime checks 
        if arg_name_to_bind not in self.function_args_aliases:
            # Any input that doesn't contribute to specifying argument to the function is considered invalid
            raise Exception("Invalid binding. ")

        if self.function_args[self.function_args_aliases[arg_name_to_bind]]["is_changeable"] == False:
            raise Exception("Invalid attempt to overide predefined argument")

        if self.function_args_aliases[arg_name_to_bind] in self.arg_prompts:
            raise Exception("Overring arg_prompt")

        self.arg_prompts[arg_name_to_bind] = arg_prompt

    def trigger(self):
        # Do base prompting
        args_to_pass = {}
        
        # Prepare arguments to pass using CLI defaults and functions defaults
        for arg_name, arg_value in self.function_args.items():
            if arg_value["default_at_cli"] != None:
                arg_value_to_pass = arg_value["default_at_cli"]
            elif arg_value["default_at_function"] != None:
                arg_value_to_pass = arg_value["default_at_function"]
            else:
                arg_value_to_pass = None

            args_to_pass[arg_name] = arg_value_to_pass

        # Prepare arguments using user inputs
        for arg_name, arg_prompt in self.arg_prompts.items():
            default_at_cli = self.function_args[arg_name]["default_at_cli"]
            args_to_pass[arg_name] = arg_prompt.trigger(default_at_cli)

        # NOTE CHECK IF ABORT SIGNAL IS RETURNED

        # Call the function
        try:
            print(f"Executing function({self.function.__name__})")
            self.function(**args_to_pass)
            utils.log_success(f"Successfully executed function({self.function.__name__})")
        except Exception as e:
            print(e)
            utils.log_failure(f"An error occcured during execution of function({self.function.__name__})")


