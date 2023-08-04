# AI GitHub Reader with ChatGPT-4

AI GitHub Reader with ChatGPT-4 is a powerful tool that allows you to explore and ask questions about a GitHub code repository using OpenAI's advanced ChatGPT-4 language model. This AI-powered assistant can provide detailed answers based on the contents of the indexed repository files, including code, text, and Jupyter Notebook files.

## Prerequisites

- Python 3.6+
- OpenAI API key (set in the environment variable OPENAI_API_KEY)

## Usage

1. Set the OpenAI API key as an environment variable `OPENAI_API_KEY`.
2. Run the script: `app.py`
3. Enter the GitHub URL of the repository you wish to explore.
4. Ask questions about the repository. To exit the program, type `exit()`.

## Key Features

- Clones and indexes the contents of a GitHub repository.
- Supports various file types, including code, text, and Jupyter Notebook files.
- Utilizes OpenAI's advanced ChatGPT-4 language model for generating highly accurate and detailed responses.
- Enables interactive conversation with the language model for iterative exploration.
- Presents top relevant documents for each question to aid understanding.

using cProfile to analyze the spatial and temporal aspects of a Python codebase. By harnessing the power of profiling, developers can make informed decisions to enhance the efficiency and speed of their applications, resulting in a more robust and performant software system.
Upon completion, the cProfile will print the profiling statistics, showing how much time was spent in each function, and helping to identify any performance bottlenecks.

Note: Profiling with cProfile may impact the execution time slightly. It's recommended to use it during development and optimization phases to fine-tune the application's performance.

## How it Works

1. The script prompts you to input the GitHub URL of the repository you want to explore.
2. It clones the repository into a temporary directory and indexes its files for faster retrieval of information.
3. The powerful ChatGPT-4 language model is used to generate detailed answers based on the indexed documents and your questions.
4. You can keep asking questions about the repository, and the AI GitHub Reader will provide relevant answers along with context information to facilitate comprehension.
