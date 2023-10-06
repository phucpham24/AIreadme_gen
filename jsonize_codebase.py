import os
import ast
import json
import subprocess


def generate_ctags_and_convert(folder_path, output_path, json_file_path):
    
    # Construct the ctags command for the current folder path and custom output path
    ctags_command = [
        'ctags',
        '-R',
        '--fields=+l',
        '--extras=+q',
        '--languages=python',
        '--output-format=json',
        '-f',
        output_path,  # Specify the custom output path here
        folder_path
    ]
    try:
        # Run the ctags command for the current folder path
        subprocess.run(ctags_command, check=True)
        print(f"CTAGs generated for folder: {folder_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating CTAGs for folder {folder_path}: {e}")

    # All CTAGs are generated in the specified custom output path (output_path)
    print(f"All CTAGs generated in: {output_path}")

    # Open JSONL file for reading
    with open(output_path, 'r') as jsonl_file:
        # Read and convert JSONL data to a list of dictionaries
        json_data = [json.loads(line) for line in jsonl_file]
    # Write the converted data to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    # Delete the JSONL file
    os.remove(output_path)


def build_hierarchy(node):
    if isinstance(node, ast.FunctionDef):
        return {
            "name": node.name,
            "type": "function",
            "calls": [],
            "children": [build_hierarchy(child) for child in node.body if isinstance(child, (ast.FunctionDef, ast.Call))]
        }
    elif isinstance(node, ast.Call) and hasattr(node.func, 'id'):
        return {
            "name": node.func.id,
            "type": "call",
            "line_number": node.lineno,
            "column_offset": node.col_offset,
            "children": []
        }
    else:
        return {}

class CallHierarchyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.call_hierarchy = {}

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.call_hierarchy[self.current_function] = build_hierarchy(node)
        self.generic_visit(node)

    def visit_Call(self, node):
        if hasattr(self, 'current_function'):
            call_info = build_hierarchy(node)
            if call_info:
                self.call_hierarchy[self.current_function]["calls"].append(call_info)
        self.generic_visit(node)

def generate_call_hierarchy(input_folder, output_file):
    # Initialize an empty dictionary to store the call hierarchy for all files
    full_call_hierarchy = {}
    try:
        # Traverse the codebase directory and process each Python file
        for root, dirs, files in os.walk(input_folder):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(root, file_name)

                    # Load and parse the Python code from the current file
                    with open(file_path, 'r') as file:
                        code_content = file.read()

                    parsed_code = ast.parse(code_content)

                    # Build the call hierarchy for the current file
                    visitor = CallHierarchyVisitor()
                    visitor.visit(parsed_code)

                    # Merge the call hierarchy for this file into the full hierarchy
                    full_call_hierarchy.update(visitor.call_hierarchy)

        # Convert the full call hierarchy to JSON
        full_call_hierarchy_json = json.dumps(full_call_hierarchy, indent=2)

        # Save the JSON data to the specified output file
        with open(output_file, 'w') as json_file:
            json_file.write(full_call_hierarchy_json)

        print("callgraph processed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def jsonize_code(folder_paths: str, output_path: str) -> str :
    
    ctag_output = 'ctag.json'
    ctag_output_path = os.path.join(output_path, ctag_output)
    callgraph_output = 'callgraph.json'
    callgraph_output_path = os.path.join(output_path, callgraph_output)
    temp_name = 'ctag.jsonl'
    temp_file = os.path.join(output_path, temp_name)
    generate_ctags_and_convert(folder_paths, temp_file, ctag_output_path)
    generate_call_hierarchy(folder_paths, callgraph_output_path)
    
    if os.path.exists(ctag_output_path):
        print(f"A new file {ctag_output} was created.")
    else:
        print("No new file was created.")
        
    if os.path.exists(callgraph_output_path):
        print(f"A new file {callgraph_output} was created.")
    else:
        print("No new file was created.")
    #output_paths_tuple = (ctag_output_path, callgraph_output_path)
    return ctag_output_path,  callgraph_output_path