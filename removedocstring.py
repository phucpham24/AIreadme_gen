import os
import re

# Define a regular expression pattern to match function definitions with docstrings
pattern = r'def (\w+)\([^)]*\):\s*\"\"\"[^\"\"\"].*?\"\"\"'

# Function to process a single Python file
def remove_docstrings_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove docstrings using regex
    modified_content = re.sub(pattern, lambda x: f'def {x.group(1)}():', content, flags=re.DOTALL)
    
    with open(file_path, 'w') as f:
        f.write(modified_content)

# Function to recursively process files in a folder
def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                remove_docstrings_from_file(file_path)

# Specify the folder path where you want to remove docstrings
folder_path = '/home/phucsaiyan/Documents/stage/test_addcomment2/'

# Call the function to process the folder
process_folder(folder_path)

