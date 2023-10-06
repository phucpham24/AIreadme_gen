import json

def extract_function_names_from_json(json_file_path):
    # Open the JSON file and load its data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Initialize a list to store function names
    function_names = []

    # Iterate through the data and extract function names
    for item in data:
        if item.get('_type') == 'tag' and item.get('kind') == 'function':
            function_names.append(item.get('name'))

    return function_names

def extract_function_detail_from_json(callgraph_file_path, function_name):
# Open and read the JSON file
    with open(callgraph_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Initialize an empty dictionary to store function details
    function_dict = {}

    # Assuming your JSON data structure follows the example you provided
    for function_name, function_data in data.items():
        # Extract function details (modify this based on your JSON structure)
        function_details = {
            "name": function_data.get("name"),
            "type": function_data.get("type"),
            "calls": function_data.get("calls"),
            "children": function_data.get("children"),
            # Add more details as needed
        }

        # Add function details to the dictionary
        function_dict[function_name] = function_details
    return function_dict

