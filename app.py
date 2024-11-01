import base64

import streamlit as st
import openai
import title_generator
import research_assistant
import data_analysis
import defense_preparation
from streamlit_option_menu import option_menu

# Configure Streamlit page
st.set_page_config(page_title="Siklab Research Hub", page_icon="📘", layout="wide")

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        # Encode the image as base64 and decode it to a string
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{image_data}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

set_background("images/Landing_page.png")

# Inject custom CSS for text and button styling with font color set to #FAFAF0
st.markdown(
    """
    <style>
    /* Button styling */
    .stButton>button { 
        background-color: #FF5733; 
        color: #FAFAF0;  /* Off-white color for button text */
        border-radius: 10px;
    }
    /* General text color for consistency */
    .css-10trblm, .css-1q8dd3e, .stTextInput, .stTextArea, .stSelectbox, h1, h2, h3, h4, h5, h6, p {
        color: #FAFAF0;  /* Off-white color for all text elements */
    }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar configuration with logo image and API key input
st.sidebar.image("images/Siklab.png", width=250)  # Replace with your image file path

# Sidebar for API key and main navigation menu
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password", key="api_key")
openai.api_key = api_key  # Set the API key globally for OpenAI

# Check if API key is valid
if not api_key or not api_key.startswith('sk-'):
    st.sidebar.warning("Please enter a valid OpenAI API key.", icon="⚠️")
else:
    st.sidebar.success("API key is valid", icon="✅")

# Define the main navigation with option_menu
with st.sidebar:
    page = option_menu(
        "Siklab Research Hub",
        ["Title Generation", "Research Paper Assistance", "Data Analysis & Visualization", "Defense Preparation"],
        icons=['file-text', 'book', 'bar-chart', 'shield'],
        menu_icon="layout-wtf",
        default_index=0,
    )

# Only proceed to load pages if a valid API key is provided
if api_key and api_key.startswith('sk-'):
    # Page navigation based on the selected page
    if page == "Title Generation":
        st.markdown(
            "<div style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; text-align: center;'>"
            "<h1 style='color: #FAFAF0;'>Title Generation</h1>"
            "<p style='color: #FAFAF0;'>Generate impactful and precise titles for your research with ease.</p>"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        #st.title("Title Generation")
        title_generator.app()  # Ensure no API key prompt exists in title_generator.py

    elif page == "Research Paper Assistance":
        st.markdown(
            "<div style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; text-align: center;'>"
            "<h1 style='color: #FAFAF0;'>Research Paper Assistance</h1>"
            "<p style='color: #FAFAF0;'>Get expert guidance through every stage of your research paper with Gilgamesh, your AI assistant.</p>"
            "</div>",
            unsafe_allow_html=True
        )

        # Add a line break for spacing
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("images/Gilgamesh.jpg", width=80)  # Set the image for Gilgamesh
        #st.title("Research Paper Assistance")
        research_assistant.app()  # Ensure no API key prompt exists in research_assistant.py

    elif page == "Data Analysis & Visualization":
        st.image("images/Casein_Nitrate.jpg", width=80)  # Set the image for Casein Nitrate
        #st.title("Data Analysis & Visualization")
        data_analysis.app()  # Ensure no API key prompt exists in data_analysis.py

    elif page == "Defense Preparation":
        st.image("images/Gilgamesh.jpg", width=80)  # Set the image for Gilgamesh for defense preparation
        #st.title("Defense Preparation")
        st.markdown(
            """
            <div style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; text-align: center;'>
                <h1 style='color: #FAFAF0; text-align: left;'>Defense Preparation</h1>
                <p style='color: #FAFAF0; text-align: left;'>
                    Gilgamesh is here to assist you prepare for your research defense by analyzing your paper and giving suggestions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        defense_preparation.app()  # Ensure no API key prompt exists in defense_preparation.py
else:
    st.warning("Please enter your OpenAI API Key in the sidebar to use the application.")
