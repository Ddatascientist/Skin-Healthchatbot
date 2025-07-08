import os
from dotenv import load_dotenv
# from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from prompt import prompt
import streamlit as st

load_dotenv()
llm_api = st.secrets["DSEEK_API"] # os.getenv("DSEEK_API")
PINECONE_API_KEY = os.getenv('PINECONE-API')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY



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

def llm_response(user_txt):
    retriever = load_store()
    llm = ChatOpenAI(
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=llm_api,
            model_name='deepseek/deepseek-r1:free',
            temperature=0.6,
            max_completion_tokens= 4000,
            streaming= True
            )
   

    llm_prompt = create_stuff_documents_chain(llm=llm, prompt=prompt)
    reatrival_llm = create_retrieval_chain(retriever, llm_prompt)

    response = reatrival_llm.invoke({"input": user_txt})
    return response['answer']