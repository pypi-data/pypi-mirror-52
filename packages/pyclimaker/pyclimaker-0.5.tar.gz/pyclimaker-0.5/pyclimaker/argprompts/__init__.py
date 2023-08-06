from .. import utils

import os



class PyCliArgPrompt():
    def __init__(self, description, return_type=str):
        self.description = description
        self.return_type = return_type

    def trigger(self, default_at_cli):
        if default_at_cli == None:
            utils.log_prompt(f"Please enter the argument:")
        # NOTE WHAT IF COMMAND IS ATTACHED WITH FLAG ARGUMENTS?
        else:
            utils.log_prompt(f"Please enter the argument. If you want to proceed with the default(={default_at_cli}), simple press ENTER:")
        
        arg = input().strip()
        if arg == "" and default_at_cli != None:
            arg = default_at_cli
        print(f"Selected argument: {arg}")

        if self.return_type == int:
            arg = int(arg)

        return arg

class PyCliFileSelectionPrompt(PyCliArgPrompt):
    def __init__(self, target_directory, description):
        self.max_len_filelist = 5
        self.target_directory = target_directory
        super().__init__(description=description)

    def trigger(self, default_at_cli):
        filenames = os.listdir(self.target_directory)
        padding = 0
        cancel_padding = 0
        while True:

            # Display filenames
            if padding != 0:
                print(0, "...See previous filenames")
            for index in range(padding, min(padding+self.max_len_filelist, len(filenames))):
                print(index - padding + 1, filenames[index])
            if padding + self.max_len_filelist < len(filenames):
                print(self.max_len_filelist+1, "...See following filenames")
                cancel_padding = 1
            print(self.max_len_filelist+1+cancel_padding, "...cancel executing the command")


            utils.log_prompt(f"Please enter index of the filename:")
            arg = input()
            
            # Check input validity
            if arg.isdigit() == False:
                utils.log_warning("Invalid input. Must an integer between A <= X <= Y")
                continue
            # NOTE elif CANCEL COMMANDS


            # Handle index argument
            if padding != 0 and int(arg) == 0:
                padding -= self.max_len_filelist
            elif padding + self.max_len_filelist < len(filenames) and int(arg) == self.max_len_filelist+1:
                padding += self.max_len_filelist
            elif int(arg) == self.max_len_filelist+cancel_padding+1:
                print("Cancelling executing command")
                break
            elif 1 <= int(arg) and int(arg) <= self.max_len_filelist:
                arg_index= int(arg) + padding - 1 
                print(f"Selected argument: {filenames[arg_index]}")
                return filenames[arg_index]
            else:
                utils.log_warning("Invalid input. Must an integer between A <= X <= Y")
                
        


