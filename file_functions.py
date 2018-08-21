import os
from glob import glob

#Returns list of sub direct subfolders from given directory
def getHtmlFolders(top_directory):
    final_directories = []
    raw_directories = [x for x in os.walk(top_directory)]
    processed_directories = raw_directories[0][1]

    for directory in processed_directories:
          final_directories.append('{}/{}'.format(top_directory, directory)) 

    final_directories.append(top_directory) #Allows for floating html files in top dir
    return final_directories


#Returns a list of all html file paths in a given folder
def globHtml(directory):
    html_files = []
    html_files.append(glob(directory + '{}'.format('/**/*.html'), recursive=True))
    return html_files[0]
