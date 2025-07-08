from flask import Flask, render_template, request
from medbot_basecode import *
import streamlit as st
from prompt import prompt

st.set_page_config(
    page_title="SM-CHATBOT",
    layout="centered",
    page_icon=":doctor:"
)

st.markdown("""
<style>
.user-msg {
    background-color: #DCF8C6;
    color: #000;
    padding: 10px 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 80%;
    align-self: flex-end;
}
.bot-msg {
    background-color: #F1F0F0;
    color: #000;
    padding: 10px 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 80%;
    align-self: flex-start;
}
</style>
""", unsafe_allow_html=True)



st.title("MED & BEAUTY-BOT")

#chat history
if "message" not in st.session_state:
    st.session_state.message = []
    
# display messages
for msg in st.session_state.message:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        

if msg := st.chat_input("Ask me any health or skin-beauty related question"):
    with st.chat_message("user"):
        st.markdown(msg)
    st.session_state.message.append({"role": "user", "content": msg})
    
    ai_res = llm_response(msg)
    result = f"SM-BOT👩‍🔬 :\n{ai_res}"
    with st.chat_message("system"):
        st.markdown(result)
    st.session_state.message.append({"role": "system", "content": result})
    
    