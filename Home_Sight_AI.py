import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv


# Setting page layout
st.set_page_config(
    page_title = "Real Estate Assistant",
    page_icon = "🏠",
    layout = "centered"
)

# Adding CSS 
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4A6FFF;
        --secondary-color: #344054;
        --accent-color: #4A6FFF;
        --background-color: #F9FAFB;
        --text-color: #1D2939;
        --light-gray: #EAECF0;
    }
    
    /* Global styles */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Title styling */
    .main-title {
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 32px;
        margin-bottom: 8px;
        padding-top: 20px;
    }
    
    .subtitle {
        color: var(--secondary-color);
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 16px;
        margin-bottom: 25px;
        opacity: 0.8;
    }
    
    /* Custom button */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #3A5CD0;
        box-shadow: 0 4px 6px rgba(74, 111, 255, 0.2);
    }
    
    .stButton>button:active {
        background-color: #2E4AAD;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 6px;
        border: 1px solid var(--light-gray);
        padding: 12px 16px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(74, 111, 255, 0.2);
    }
    
    /* Response container */
    .response-container {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.1);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Setting API key 
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key = GEMINI_API_KEY)

# Adding header
st.markdown("<div class = 'main-title'> Home Sight AI </div>", unsafe_allow_html = True)
st.markdown("<div class = 'subtitle'> Powered by Google Gemini AI </div>", unsafe_allow_html = True)

def retriever_info(query):
    return "Latest real estate trends including property market analysis, investment opportunities, " \
           "housing demand and supply dynamics, mortgage rates updates, commercial real estate developments, " \
           "urban planning innovations, sustainable architecture trends, rental market insights, and emerging property technologies."

# Generating Information
def rag_query(query):
    retrieved_info = retriever_info(query)
    augmented_prompt = f"User query about real estate and properties:\n{query}\nRetrieved information:\n{retrieved_info}"
    
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    response = model.generate_content(augmented_prompt)
    
    return response.text.strip()

# User input 
st.markdown("### Ask a question about Real Estate")
user_input = st.text_input("", placeholder = "Type Your Query Here...", key = "query_input")

# Submit button 
if st.button("Generate Response", key="submit_button"):
    if user_input:
        with st.spinner("Generating insights..."):
            response = rag_query(user_input)
        
        st.markdown("<div class = 'response-container'>", unsafe_allow_html = True)
        st.markdown("### AI Response")
        st.write(response)
        st.markdown("</div>", unsafe_allow_html = True)
    else:
        st.warning("Please enter a question to continue.")
