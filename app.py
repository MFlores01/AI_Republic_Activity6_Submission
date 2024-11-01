import streamlit as st
from streamlit_option_menu import option_menu
from multiapp import MultiApp
from pages import title_generator, research_assistant, data_analysis, defense_preparation

# Configure Streamlit page
st.set_page_config(page_title="Research Assistant Hub", page_icon="📘", layout="wide")

# Sidebar configuration with logo image and API key input
st.sidebar.image("images/Siklab.png", width=250)  # Replace with your image file path

# Sidebar for API key and navigation
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
app = MultiApp(api_key=api_key)  # Pass API key to app for OpenAI access

# Define sidebar menu with option_menu
with st.sidebar:
    page = option_menu(
        "Research Assistant Hub",
        ["Title Generation & Scrutiny", "Research Paper Assistance", "Data Analysis & Visualization", "Defense Preparation"],
        icons=['file-text', 'book', 'bar-chart', 'shield'],
        menu_icon="layout-wtf",
        default_index=0,
    )

# Warning if no API key is entered
if not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to use the application.")

# Page navigation
else:
    if page == "Title Generation & Scrutiny":
        st.title("Title Generation & Scrutiny")
        st.markdown("""
            This page assists you in generating unique and compelling research titles and provides a detailed critique to prepare you for title defense.
        """)
        title_generator.app(api_key=api_key)  # Call the title generation page function with the API key

    elif page == "Research Paper Assistance":
        st.image("images/Gilgamesh.jpg", width=80)
        st.title("Research Paper Assistance (Gilgamesh)")
        st.markdown("""
            Gilgamesh, your research assistant, will guide you through each section of your research paper, from introduction to methodology and more.
        """)
        research_assistant.app(api_key=api_key)  # Call the research assistant page function with the API key

    elif page == "Data Analysis & Visualization":
        st.image("images/Casein_Nitrate.jpg", width=80)
        st.title("Data Analysis & Visualization (Casein Nitrate)")
        st.markdown("""
            Casein Nitrate, your data analysis assistant, helps you explore, analyze, and visualize your dataset with detailed insights.
        """)
        data_analysis.app(api_key=api_key)  # Call the data analysis page function with the API key

    elif page == "Defense Preparation":
        st.title("Defense Preparation")
        st.markdown("""
            Prepare for your research or thesis defense with Gilgamesh's in-depth critique and potential panel questions.
        """)
        defense_preparation.app(api_key=api_key)  # Call the defense preparation page function with the API key
