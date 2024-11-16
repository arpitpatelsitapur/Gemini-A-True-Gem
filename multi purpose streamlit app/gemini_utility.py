import os
import json
import google.generativeai as genai
from PIL import Image
wdir=os.path.dirname(os.path.abspath(__file__))

config_filepath=f"{wdir}/config.json"
config_data=json.load(open(config_filepath))

GOOGLE_API_KEY=config_data['GOOGLE_API_KEY']

genai.configure(api_key=GOOGLE_API_KEY)

def load_gemini_pro_model():
    model=genai.GenerativeModel('gemini-pro')
    return model

def gemini_flash_response(prompt,image):
    flash_model=genai.GenerativeModel("gemini-1.5-flash")
    response=flash_model.generate_content([prompt,image])
    result=response.text
    return result

def load_embeddings(input_text):
    embedding_model='models/embedding-001'
    embeddings=genai.embed_content(
        model=embedding_model,
        content=input_text,
        task_type='retrieval_document'
    )
    embedding_list=embeddings['embedding']
    return embedding_list


def gemini_response(query):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(query)
    return response.text


