import streamlit as st
import openai
import title_generator
import research_assistant
import data_analysis
import defense_preparation
from streamlit_option_menu import option_menu

# Configure Streamlit page
st.set_page_config(page_title="Research Assistant Hub", page_icon="📘", layout="wide")

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
        ["Title Generation & Scrutiny", "Research Paper Assistance", "Data Analysis & Visualization", "Defense Preparation"],
        icons=['file-text', 'book', 'bar-chart', 'shield'],
        menu_icon="layout-wtf",
        default_index=0,
    )

# Only proceed to load pages if a valid API key is provided
if api_key and api_key.startswith('sk-'):
    # Page navigation based on the selected page
    if page == "Title Generation & Scrutiny":
        st.title("Title Generation & Scrutiny")
        title_generator.app()  # Ensure no API key prompt exists in title_generator.py

    elif page == "Research Paper Assistance":
        st.image("images/Gilgamesh.jpg", width=80)  # Set the image for Gilgamesh
        st.title("Research Paper Assistance")
        research_assistant.app()  # Ensure no API key prompt exists in research_assistant.py

    elif page == "Data Analysis & Visualization":
        st.image("images/Casein_Nitrate.jpg", width=80)  # Set the image for Casein Nitrate
        st.title("Data Analysis & Visualization")
        data_analysis.app()  # Ensure no API key prompt exists in data_analysis.py

    elif page == "Defense Preparation":
        st.image("images/Gilgamesh.jpg", width=80)  # Set the image for Gilgamesh for defense preparation
        st.title("Defense Preparation")
        defense_preparation.app()  # Ensure no API key prompt exists in defense_preparation.py
else:
    st.warning("Please enter your OpenAI API Key in the sidebar to use the application.")
