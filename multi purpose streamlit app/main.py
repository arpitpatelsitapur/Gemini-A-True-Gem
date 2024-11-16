import streamlit as st
import os
from streamlit_option_menu import option_menu
from PIL import Image
from gemini_utility import (load_gemini_pro_model,
                            gemini_flash_response,
                            load_embeddings,
                            gemini_response)

working_directory=os.path.dirname(os.path.abspath(__file__))

# setting page configuaration
st.set_page_config(
    page_icon="",
    page_title="Multi-Purpose Chatbot",
    layout="centered"
)
with st.sidebar:
    selected=option_menu(
        menu_title="Select Purpose",
        options=[
            "Chatbot",
            "Image Captioning",
            "Text Embedding",
            "Ask me anything"
        ],
        menu_icon="robot",
        icons=["chat-dots-fill",
               'image-fill',
               'textarea-t',
               "patch-question-fill"],
               default_index=0
    )

def translate_role_for_streamlit(user_role):
    if (user_role=='model'):
        return 'assistant'
    else:
        return user_role

if selected=='Chatbot':
    model=load_gemini_pro_model()

    if 'chat_session' not in st.session_state:
        st.session_state.chat_session=model.start_chat(history=[])

    st.title("ChatBot")
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt=st.chat_input("What is Your Query???")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response=st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message('assistant'):
            st.markdown(gemini_response.text)

elif selected=='Image Captioning':
    st.title('Snap Narrator')
    uploaded_image=st.file_uploader('Upload an Image....',type=['jpg','png','jpeg'])

    if st.button('Let LLM think what is it.'):
        image=Image.open(uploaded_image)
        col1,col2=st.columns(2)
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        default_prompt="write single most matching short caption about this image."
        caption=gemini_flash_response(default_prompt,image)
        with col2:
            st.info(caption)

elif selected=='Text Embedding':
    st.title("Check samples of Text Embeddings.")
    st.markdown("Here we used **`Generative AI Models/Embedding-001`**. The token size of Embedding-001 is **1024** and the **embedding length is 768** due to the fact that the model uses a special token called a [CLS] token. This token is added to the beginning of the input sequence and is used to represent the overall meaning of the sentence.")
    input_text=st.text_area(label='Input Text',placeholder='Enter Sample Text...')
    if st.button("Get Embeddings"):
        response=load_embeddings(input_text)
        #st.markdown(len(response))
        st.markdown(response)

else:
    st.title("Ask your query, but remember no session history saved here.")
    query=st.text_input("Ask your Query...")
    if st.button('Get Response'):
        response=gemini_response(query)
        st.markdown(response)





