# questions.py
from utils import format_documents
from file_processing import search_documents

class QuestionContext:
    def __init__(self, index, documents, llm_chain, model_name, function_name, function_detail, file_type_counts, filenames):
        self.index = index
        self.documents = documents
        self.llm_chain = llm_chain
        self.model_name = model_name
        self.function_name = function_name
        self.function_detail = function_detail
        self.file_type_counts = file_type_counts
        self.filenames = filenames

def ask_question(question, context: QuestionContext):
    relevant_docs = search_documents(question, context.index, context.documents, n_results=5)

    numbered_documents = format_documents(relevant_docs)
    question_context = f"This function is '{context.function_name}' and function detail {context.function_detail}. The most relevant documents are:\n\n{numbered_documents}"

    answer_with_sources = context.llm_chain.run(
        model=context.model_name,
        question=question,
        context=question_context,
        function_detail=context.function_detail,
        function_name=context.function_name,
        numbered_documents=numbered_documents,
        file_type_counts=context.file_type_counts,
        filenames=context.filenames
    )
    return answer_with_sources