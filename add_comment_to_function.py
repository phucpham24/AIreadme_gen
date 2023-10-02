# Import the regular expressions module for pattern matching
import re

# Function to add a docstring before a function
def add_docstring_to_function(file_path, function_name, docstring):
    with open(file_path, 'r') as source_file:
        lines = source_file.readlines()

    in_function = False
    modified_lines = []

    for line in lines:
        # Check if the current line contains the function name
        if re.match(r'^\s*def\s+' + re.escape(function_name) + r'\s*\(.*\):', line):
            in_function = True
            modified_lines.append(f'def {function_name}():\n')
            modified_lines.append(f'    """{docstring}"""\n')  # Add the docstring
        elif in_function:
            # Copy the rest of the function
            modified_lines.append(line)
        else:
            modified_lines.append(line)

    with open(file_path, 'w') as source_file:
        source_file.writelines(modified_lines)

# Define the path to your ctags file
ctags_file_path = '/home/phucsaiyan/Documents/stage/clonechatgpt/tags'  # Update with the actual path to your ctags file

# Function name to search for
function_to_search = 'clone_github_repo'  # Replace with the name of the function you want to find

# Docstring to add to the function
docstring_to_add = 'clone test'

# Read the ctags file and find the function's location
with open(ctags_file_path, 'r') as ctags_file:
    for line in ctags_file:
        parts = line.strip().split('\t')
        if len(parts) >= 4 and parts[0] == function_to_search:
            file_path = parts[1]
            # Add a docstring to the function
            add_docstring_to_function(file_path, function_to_search, docstring_to_add)
            print(f"Docstring added to function '{function_to_search}' in {file_path}")
            break