import os
import openai
import re
import json
from dotenv import load_dotenv
from file_processing import load_and_index_files, search_documents
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from config import WHITE, GREEN, RESET_COLOR, model_name
from utils import format_user_question
from questions import ask_question, QuestionContext
# Define your OpenAI API key

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to read ctags file and extract function names and locations
def extract_functions_from_ctags(ctags_file):
    functions = []
    with open(ctags_file, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                name, _, location = parts[:3]
                functions.append((name, location))
    return functions

# Function to read call hierarchy JSON file
def read_call_hierarchy_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    # Process the JSON data as needed to extract relevant information
    return data  # Return the loaded JSON data

# Function to generate text using OpenAI API with text splitter
def generate_text_with_splitter(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100  # Adjust the max_tokens as needed
    )
    return response.choices[0].text.strip()

      
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

# Main function
def main():
    folder_path = "/home/phucsaiyan/Documents/stage/test_addcomment2"  # Specify the folder path here
    ctags_file = os.path.join(folder_path, "/home/phucsaiyan/Documents/stage/test_addcomment/tags")
    json_file = os.path.join(folder_path, "/home/phucsaiyan/Documents/stage/test_addcomment/full_call_hierarchy.json")
    
    try:
        functions = extract_functions_from_ctags(ctags_file)
        call_hierarchy_data = read_call_hierarchy_json(json_file)

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(".py"):
                    code_file_path = os.path.join(root, file_name)

                    for function_name, _ in functions:
                        # Use the call hierarchy data to determine which functions need docstrings
                        if function_name in call_hierarchy_data:
                            prompt = f"Generate a comment for the function {function_name} based on call hierarchy data:\n\n{call_hierarchy_data}"
                            generated_text = generate_text_with_splitter(prompt)
                            add_docstring_to_function(code_file_path, function_name, generated_text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
if __name__ == "__main__":
    main()