import os
from dotenv import load_dotenv
# from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from prompt import prompt
import streamlit as st

load_dotenv()
llm_api = st.secrets["DSEEK_API"] # os.getenv("DSEEK_API")
os.environ["PINECONE_API_KEY"] = os.getenv('PINECONE-API')
os.environ["GOOGLE_API_KEY"] = os.getenv('GEMINI_API')



def load_store():
    model_embed = HuggingFaceEmbeddings()
    index_name = "med-skincare-chatbot"

    vector_store = PineconeVectorStore.from_existing_index(
        index_name=index_name, 
        embedding=model_embed,
        # namespace="chatbot"
        )
    
    retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
    )
    
    return retriever

def choose_llm(c_llm: str):
    if c_llm.lower() == "deepseek":
        llm = ChatOpenAI(
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=llm_api,
            model_name='deepseek/deepseek-r1:free',
            temperature=0.6,
            max_completion_tokens= 4000,
            streaming= True
            )
        return llm
        
    elif c_llm.lower() == "gemini":
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.6,
            max_tokens=4000,
            timeout=None,
            max_retries=3,
            # other params...
        )
        return llm
    else:
        return "Please specify between 'gemini' or 'deepseek'."

def llm_response(user_txt):
    retriever = load_store()
    llm = choose_llm("deepseek")
   

    llm_prompt = create_stuff_documents_chain(llm=llm, prompt=prompt)
    reatrival_llm = create_retrieval_chain(retriever, llm_prompt)

    response = reatrival_llm.invoke({"input": user_txt})
    return response['answer']