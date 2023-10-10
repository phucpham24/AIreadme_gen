import os
import openai
from dotenv import load_dotenv
from file_processing import load_and_index_files
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from jsonize_codebase import jsonize_code, generate_ctags_and_convert, generate_call_hierarchy
from extract_info import extract_function_names_from_json, extract_function_detail_from_json
from questions import ask_question, QuestionContext
from utils import format_user_question
from adddocstring import add_docstring_to_function
from config import model_name, GREEN, RESET_COLOR, WHITE 
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    github_url = input("enter local path of this repo: ")
    repo_name = github_url.rsplit("/", 1)[-1]
    output_path = github_url
    ctag_path,callgraph_path = jsonize_code(github_url, output_path)

    print("jsonize code is done")

    functions = extract_function_names_from_json(ctag_path)
    index, documents, file_type_counts, filenames = load_and_index_files(github_url)
    if index is None:
        print("No documents were found to index. Exiting.")
        exit()


    for function_name in functions: 
        function_dict = extract_function_detail_from_json(callgraph_path, function_name)
        llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.2)
        function_detail = function_dict[function_name]
        template = """
        Repo: name: {function_name} | details: {function_detail} | Docs: {numbered_documents} | Q: {question} | FileCount: {file_type_counts} | FileNames: {filenames}
        Instr:
        Brief description of the function.

            More detailed description of the function, including its purpose,
            input parameters, and return value.

            Parameters:
            ----------
            parameter1 : data_type
                Description of parameter1.
            parameter2 : data_type
                Description of parameter2.

            Returns:
            -------
            return_type
                Description of the return value.

        """
        prompt = PromptTemplate(
            template=template,
            input_variables=[ "function_name", "function_detail", "question", "numbered_documents",
                              "file_type_counts", "filenames"]
        )
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        question_context = QuestionContext(index, documents, llm_chain, model_name, function_name, function_detail, file_type_counts, filenames)
        user_question = f"generate a docstring for the function: {function_name} "
        user_question = format_user_question(user_question)  
        answer = ask_question(user_question, question_context)
        print(function_name)
        print(user_question)
        print(GREEN + '\nANSWER\n' + answer + RESET_COLOR + '\n')
        add_docstring_to_function(github_url, function_name, answer)

