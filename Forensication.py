#Imports
import subprocess
import json

file_path = "Information.txt" #The name of the file that stores all the data.
format = "-"*70 #Line seperator
admin_command = "Get-LocalGroupMember -Name 'administrators' | ConvertTo-Json" #Powershell command - Gets the local users from the "administrators" group.
network_command = "Get-WmiObject win32_networkadapterconfiguration | ConvertTo-Json"#Powershell command - Gets information about the network adapters in the computer.
vid_pid_command = "Get-ChildItem -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\USB' | ConvertTo-Json" #Powershell command - Gets all the Vid/Pids located in ENUM/USB.


#def A funcions to get the users from the group "administrators".
def get_local_administrators():
    write_to_file(file_path,"a","Local Administrators: \n") #Calls the write_to_file function with the given parameters.
    creating_format(admin_command,["PrincipalSource"]) #Calls the creating_format function with the given arguments
        

#def Get network information - adapters information
def get_network_information():
    write_to_file(file_path,"a","Network Adapters Information: \n") #Calls the write_to_file function with the given parameters.
    creating_format(network_command,["Qualifiers", "SystemProperties", "Properties","ClassPath","Options","Path","Scope"]) #Calls the creating_format function with the given arguments.


#Function that goes to the regedit vid&pid keys and collects data.
def get_regedit_vid():
    write_to_file(file_path,"a","Vid&Pid Connected:" + "\n") #Calls the write_to_file function with the given parameters.
    creating_format(vid_pid_command,["PSChildName","Name"],True) #Calls the creating_format function with the given arguments.

#A function to inject a powershell command and return a decoded output
#Given parameters:
#@command - powershell command
def inject_powershell_command(command): 
    #Declares a variable to store the data from the powershell command that is ran by subprocess.
    output = subprocess.run(["powershell.exe","-Command",command],capture_output=True) 
    decoded_output = output.stdout.decode("UTF-8") #Decodes the data to UTF-8 from binary.
    return decoded_output #Returns that data

#Clearing spaces
#Given arguments:
#@file_name = the name of the file to edit (declared at the start of the code).
def clear_spaces(file_name):
    holder = "" #String holder
    with open(file_name,"r") as f: #Opens the file with read permissions.
        for line in f: #Loops Through all the line in the file.
            if not line.isspace(): #Checks if the line isnt space.
                holder += line #Adds the line to the string holder.
        
    with open(file_name,"w") as f: #Opens the file with write permissions.
        f.writelines(holder) #Writes all the non space lines.

#Function to write the data to a file. 
# path -> file path
# option -> 'a'/'w'/'r' - options to open the file.
#data -> the data given to write to the file.
def write_to_file(path,option,data):
    with open(path,option) as file: #Opens the file with the given permissions.
        file.write(data) #Write the data.

#Function to format powershell command output into json and outputing it.
#Given arguments -> d:^)
#@exeptions -> telling the program to ignore specific keys in the dict (list).
#@command -> the command that will be sent to the inject_powershell_command function.
#@reverse -> argument with the defualt set as False, if given true, selecting specific keys and adding just them
#to the propertirs instead of skipping them.
#returing json format
def creating_format(command, exeptions,reverse=False):
    padding = 0 #Variable
    properties = [] #Empty list
    powershell_ouput = inject_powershell_command(command) #Calls the inject_powershell_command and stores it to a variable.
    
    result = json.loads(powershell_ouput) #Loads the file into a json format and stores it to a variable.
    for i in result[0].keys(): #Loops through all the keys in the dict (the dict is the first index of a list).
        if(not reverse): #Checking if the reverse boolean is set to default(false).
            if i in exeptions: #Checks if i is in the list of exeptions to ignore.
                continue #Continue if they are in the exeptions.
            properties.append(i) #Adds the rest of the properties list.
            if len(i) > padding: #Checks if the len of the word is longer and sets the padding accordingly.
                padding = len(i) #Sets the padding to the len of the word.
        elif(reverse): #Checks if the reverse argument was declared as True.
            if i in exeptions: #if i is in the list of exeptions.
                properties.append(i) #Add only the keys in the list of exeptions (unlike ignoring them when reverse is False).
            if len(i) > padding: #Checks if the len of the word is longer and sets the padding accordingly.
                padding = len(i) #Sets the padding to the len of the word.

    
    for i in result: #Loops through the entire json output
        for property in properties: #Loops through the list of properties that was set above.
            if(i[property] == None):#Checks if the value is null.
                continue #Skip
            else:
                data = (f'{property.ljust(padding)}' + ":" + f'{i[property]}' + "\n") #Formats the output to be equal length by the len of the longest word.
                write_to_file(file_path,"a",data) #Calls the write_to_file function with the given parameters.
                continue
        write_to_file(file_path,"a",format+"\n") #Calls the write_to_file function with the given parameters.


#Main function of the program.
def main(): 
    #Calling Functions.
    write_to_file(file_path,"w","")
    get_local_administrators() 
    clear_spaces(file_path)
    get_network_information()
    get_regedit_vid()


#Main loop.
if __name__ == "__main__":
    main() #Calling main.

