# AI Codebase Reader with ChatGPT-4

AI GitHub Reader with ChatGPT-4 is a powerful tool that allows you to explore your code using OpenAI's advanced ChatGPT-4 language model. This AI-powered assistant can provide detailed answers based on the contents of the indexed repository files, including code, text, and Jupyter Notebook files.

## Prerequisites

- Python 3.6+
- OpenAI API key (set in the environment variable OPENAI_API_KEY)

## Usage

1. Set the OpenAI API key as an environment variable `OPENAI_API_KEY`.
2. Run the script: `app.py`

## Workflow Steps
1. **Codebase Analysis**: The application begins by analyzing the codebase. It creates a call hierarchy and utilizes ctags to identify all the functions present in the code. This step is crucial for understanding the structure of the code and the functions that need docstrings.

2. **Tokenization and Similarity**: Next, the existing documentation is parsed and splitted all the code and documents by LlamaIndex, tokenizes them into vectors, and compares the similarity between these tokens and a given question. This helps in understanding the context and relevance of the question to the code.

3. **OpenAI API Integration**: The application then connects to the OpenAI API. It sends the function, function details, and code extracts to query the API with the specific question related to docstring generation. This question typically asks for a description of what the function does and the parameters it accepts.

4. **Docstring Addition**: After receiving responses from the OpenAI API, the application automatically adds the generated docstring to each function in the codebase. This enhances code documentation, making it more accessible and understandable.


## Future Work
**Handling Large Codebases**: Currently, the tool may not work efficiently with massive codebases due to context window limitations. Future work involves optimizing the tool to handle larger codebases more effectively. This could include refining the process of adjusting and controlling the documents sent to the OpenAI API.

**Expanding Code Language Support**: To make the tool more versatile, consider expanding its capabilities to generate docstrings for different programming languages beyond the current scope. Supporting languages like JavaScript, C++, Dart, and more would enhance its utility.

**Multiplying Input for Code**: Enhance the tool's ability to process multiple input types of code simultaneously. This could involve improving parallel processing to generate docstrings for multiple functions or code snippets concurrently.

**Multi-threading Support**: Introduce multi-threading capabilities to the tool to allow it to generate docstrings for multiple functions at the same time. This would significantly improve efficiency, especially for projects with a large number of functions to document.
