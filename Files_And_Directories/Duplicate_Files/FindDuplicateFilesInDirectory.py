#!/usr/bin/python

'''
A python script to get duplicate files by comparing hashes of files in all sub-directories of a directory
'''

import hashlib
import os
import json
import PySimpleGUI as sg

All_Files_Hash ={}

def Get_MD5_File_Hash(FilePath):
    hash_md5 = hashlib.md5()
    try:
        with open(FilePath,"rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
    except Exception as ex:
        print(ex)
        return "ss"
    return hash_md5.hexdigest()

def Generate_Hashes_Of_Files_And_Search_Duplicates(rootDirPath):
    for dir, subDir, files in os.walk(rootDirPath):
        for file in files:
            filePath = os.path.join(dir,file)
            fileHash = Get_MD5_File_Hash(filePath)
            if(fileHash=="ss"):
                continue
            if fileHash in All_Files_Hash:
                All_Files_Hash[fileHash].append(filePath)
                print(f"Duplicate: {All_Files_Hash[fileHash]}")
            else:
                temp=[]
                temp.append(filePath)
                All_Files_Hash[fileHash]=temp

#Needs some work
def Save_Data_To_JSON_File():
    with open("DuplicateFiles.json","w+") as f:
        json.dump(All_Files_Hash,f,indent=4)


def Save_Data_To_File(DirectoryPath):
    file_name = os.path.join(DirectoryPath,"DuplicateFiles.txt")
    with open(file_name,"w") as f:
        for val in All_Files_Hash.values():
            if len(val) > 1:
                f.write("Duplicates\n")
                for l in val:
                    f.write(l)
                    f.write("\n")
                f.write("\n\n\n")
    return file_name


if __name__ == "__main__":
    layout = [  [sg.Text('Choose the directory'),sg.Input(),sg.FolderBrowse()],
            [sg.Button('OK'), sg.Button('Cancel')]
        ]

# Create the GUI Window Prompt
    window = sg.Window('Input', layout)
    valid = False
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        # Here we read the path of the folder
        DirectoryPath = values[0]

        if event in (None, 'Cancel'):	# if user closes window or clicks cancel
            sg.Popup("Exiting..")            
            window.close()
            exit()

        if event == "OK":
            if values[0] == "":
                sg.Popup("Enter value", "Choose directory to find duplicate files ")
            else:
                valid=True
    
        if valid==True:
            Generate_Hashes_Of_Files_And_Search_Duplicates(DirectoryPath)
            #print('You entered ', values[0])
            break    

    window.close()

    while(os.path.exists(DirectoryPath)==False):
        DirectoryPath = input("Enter full path of directory to search: ")
        if(os.path.exists(DirectoryPath)==False):
            print(f"Path '{DirectoryPath}' does not exist!")
    print("Search started to find duplicates...")
    #Generate_Hashes_Of_Files_And_Search_Duplicates(DirectoryPath)
    #Save_Data_To_JSON_File()


    if not All_Files_Hash:
        sg.Popup("No duplicate files were found")
    else:
        #print(All_Files_Hash)
        file_name = Save_Data_To_File(DirectoryPath)
        sg.Popup("Result","Result stored in file {}".format(file_name))
    #pause = input("Search Completed. Press any key to continue!!")