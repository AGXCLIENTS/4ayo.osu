import os
import fnmatch

def search_string_in_files(folder, file_extension, search_string):
    for root, dirs, files in os.walk(folder):
        for file_name in fnmatch.filter(files, f"*.{file_extension}"):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_number, line in enumerate(file, start=1):
                    if search_string in line:
                        print(f'Found in file: {file_path}, line: {line_number}')
                        print(line)

# Replace 'your_folder_path' with the path to the folder you want to search in
folder_path = './'
file_extension = 'py'
search_string = 'player.id'

search_string_in_files(folder_path, file_extension, search_string)
