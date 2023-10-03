import ast
import json
import os

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

# Specify the directory where your codebase is located
codebase_directory = '/home/phucsaiyan/Documents/aider/aider/aider'

# Initialize an empty dictionary to store the call hierarchy for all files
full_call_hierarchy = {}

# Traverse the codebase directory and process each Python file
for root, dirs, files in os.walk(codebase_directory):
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

# Save the JSON data to a file or use it as needed
with open('full_call_hierarchy.json', 'w') as json_file:
    json_file.write(full_call_hierarchy_json)