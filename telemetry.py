#########################
# Author: IPvZero       #
#########################

from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.files import write_file
from datetime import date
import pathlib
import os
import colorama
from colorama import Fore, Style
from pyfiglet import Figlet

#Clear the terminal screen
clear_command = "clear"
os.system(clear_command)

#Print the words "Nornir is gathering telemetry" with ASCII art
sub_fig = Figlet(font='digital')
print(sub_fig.renderText('''Nornir is gathering telemetry...'''))

#Define the function called "backup_configurations with the argument "task"
def backup_configurations(task):
    #specify the command out you want to archive - edit these commands to fit your needs
    commands = "show run", "show cdp neighbor detail", "show version", "show clock", "show logging"
    #create For Loop to iterate through commands
    for cmd in commands:
        name = str(cmd)
        #replace with whitespace between words with hyphens for the folder output
        folder = name.replace(" ", "-")
        #create a variable with the string value "config-archive"
        config_dir = "config-archive"
        #create variable for timestamped subdirectory with the day's date
        date_dir = config_dir + "/" + str(date.today())
        #create variable within the date directory named after the command executed
        command_dir = date_dir + "/" + folder
        #use pathlib to create directory structure using the above variables
        pathlib.Path(config_dir).mkdir(exist_ok=True)
        pathlib.Path(date_dir).mkdir(exist_ok=True)
        pathlib.Path(command_dir).mkdir(exist_ok=True)
        #use scrapli to deploy commands and save output to the variable "r"
        r = task.run(task=send_command, command=cmd)
        #write the output to a textfile taking the output of the "r" variable as the input
        #name the file after the devices hostname and appended that to ".txt"
        task.run(
            task=write_file,
            content=r.result,
            filename=f"" + str(command_dir) + "/" + task.host.name + ".txt",
     )

#initialise Nornir and specify the configuration file to use
nr = InitNornir(config_file="config.yaml")

#instruct Nornir to execute the "backup_configurations" function create above
result = nr.run(
    name="Creating Backup Archive", task=backup_configurations
)

#clear the terminal screen
os.system(clear_command)
#print "Archive Created" in Green text once task has completed
print(Fore.GREEN + "Archive Created")
