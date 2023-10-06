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