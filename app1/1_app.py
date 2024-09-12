import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# streamlit app 
st.set_page_config(
    page_icon="brain",
    page_title="Simple Chabot using Gemini Pro API",
    layout="centered"
)


GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

# setup gemini model
genai.configure(api_key=GOOGLE_API_KEY)

model=genai.GenerativeModel('gemini-pro')

# function to transfer role b/w gemini and user
def translate_role_for_stramlit(user_role):
    if user_role=='model':
        return "assistant"
    else:
        return user_role
    

# initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session=model.start_chat(history=[])

# app ui
st.title("🤖 Gemini Pro Chatbot")

# display chat history

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_stramlit(message.role)):
        st.markdown(message.parts[0].text)

# input by user
user_input=st.chat_input("Ask to Gemini Pro........")
if user_input:
    # add user message to chat
    st.chat_message("user").markdown(user_input)

    # get output
    response=st.session_state.chat_session.send_message(user_input)

    # show output
    with st.chat_message('assistant'):
        st.markdown(response.text)



