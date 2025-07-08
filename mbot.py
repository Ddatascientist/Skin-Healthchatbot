from flask import Flask, render_template, request
from medbot_basecode import *
import streamlit as st
from prompt import prompt

st.set_page_config(
    page_title="SM-CHATBOT",
    layout="centered",
    page_icon=":doctor:"
)

st.title("MED & BEAUTY-BOT")

#chat history
if "message" not in st.session_state:
    st.session_state.message = []
    
# display messages
for msg in st.session_state.message:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        

if msg := st.chat_input("Ask me any health or skin-beauty related question"):
    with st.chat_message("user"):
        st.markdown(msg)
    st.session_state.message.append({"role": "user", "content": msg})
    
    ai_res = llm_response(msg)
    result = f"SM-BOT👩‍🔬 :\n{ai_res}"
    with st.chat_message("system"):
        st.markdown(result)
    st.session_state.message.append({"role": "system", "content": result})
    
    