import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"  # LangSmith tracking

# Streamlit app configuration
st.set_page_config(
    page_icon="brain",
    page_title="GGV Campus Chatbot using Gemini Pro API",
    layout="centered"
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Setup Gemini model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Function to translate role for Streamlit chat
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role

# Initialize chat session and preloaded context
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    
# Predefined context for GGV-related queries (not displayed)
context = """
The Institute of Technology GGV, located in Koni, Bilaspur, is a hub of academic activity with numerous resources and services available for students. 
The campus is 1.4 km from the main gate, a 20-minute walk, and 8.9 km from Uslapur railway station, while Bilaspur junction is 11 km away. 
For administrative needs like issuing transfer certificates, students can approach the final year departmental coordinator, while queries about campus amenities such as washrooms or e-classrooms can be directed to the departmental coordinator as well. 
Complaints about facilities, including washroom cleaning, should be addressed to the Head of Department through a formal application. 
Students can book e-classrooms for events by submitting an application to the Dean of the School. Wi-Fi services, library facilities, and other amenities are managed by the respective staff, and technical support for portal access is handled by departmental coordinators.

For student activities, details about societies and clubs can be found on the GGV website or through respective senior members. 
Admission and placement-related questions should be directed to the Admission Coordinator or Placement Coordinator, while medical emergencies require contacting the Head of Department. 
Hostel allotment is merit-based for freshers, and old students can secure accommodation if they were previously hostel residents. 
The campus library operates from 8 am to 8 pm, and the office hours are from 10 am to 6 pm, Monday to Friday. 
For food services, the Swabhiman Thali offers meals between 12:30 PM and 3:00 PM, with a charge of ₹10 per meal, although online booking is not available.

Course registration for each semester can be completed through the Samarth portal, and any complaints regarding answer sheets can be addressed to the Dean through the Head of Department. 
The university holds an A++ NAAC ranking, offering BTech and MTech programs with fees around ₹1,25,000 and ₹71,000 respectively. 
Scholarships like the state scholarships, NSP, and Siemens Scholarship are available to eligible students. 
For bonafide certificates, students should submit an application to the department office. Wi-Fi connectivity is available on campus through MHRD, and students can register for access.
"""

# App UI
st.title("🤖 GGV Campus Chatbot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input from the user
user_input = st.chat_input("Ask a question about GGV...")

if user_input:
    # Add user message to chat
    st.chat_message("user").markdown(user_input)
    
    # Send message with context to the Gemini model
    full_input = f"Context: {context}\n\nQuestion: {user_input}"

    # Get response from the model
    response = st.session_state.chat_session.send_message(full_input)

    # Show assistant's response
    with st.chat_message('assistant'):
        st.markdown(response.text)