from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "You are a medical assistance, expert in medical question-answering task."
    "You are to answer questions from the retrieval documents."
    "if a question is out of context or can't be found from retrieved documents, simply answer with 'I don't know'"
    "Ensure to keep your answers short and precise"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)