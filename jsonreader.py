import json

# Specify the path to your JSON file
file_path = '/home/phucsaiyan/Documents/stage/clonechatgpt/output.json'

try:
    # Open the JSON file
    with open(file_path, 'r', encoding='utf-8') as json_file:
        # Read the JSON data
        data = json.load(json_file)
        
        # Now, 'data' contains the JSON content as a Python object (dictionary or list)
        print(data)
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")