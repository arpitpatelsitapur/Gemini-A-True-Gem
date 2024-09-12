# langchain integration in geminipro
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"  # LangSmith tracking

# Streamlit app setup
st.set_page_config(
    page_icon="brain",
    page_title="Langchain and Gemini Pro API",
    layout="centered"
)

# Get Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Setup Gemini Pro with Langchain support
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# Define a prompt template for content creation (tweet generation in this case)
tweet_prompt = PromptTemplate.from_template("You are a content creator. Write me a tweet about {topic}.")

# Chain setup with Langchain
tweet_chain = LLMChain(llm=llm, prompt=tweet_prompt, verbose=True)

# Streamlit UI Title
st.title("🤖 Gemini Pro Content Creator using Langchain")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to display chat history in Streamlit
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input field
user_input = st.chat_input("Enter a topic to generate a tweet...")

# On user input, run the chain and display the result
if user_input:
    # Add user message to session state
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Generate tweet based on the input topic
    response = tweet_chain.run(topic=user_input)
    
    # Add response to session state
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Display the output in chat format
    with st.chat_message("assistant"):
        st.markdown(response)