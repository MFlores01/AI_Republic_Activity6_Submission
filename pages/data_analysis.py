import streamlit as st
import pandas as pd
import openai
from io import BytesIO
import matplotlib.pyplot as plt

def app():
    st.title("Data Analysis & Visualization (Casein Nitrate)")

    uploaded_file = st.file_uploader("Upload your data file (CSV, Excel, JSON, etc.):", type=["csv", "xlsx", "json"])

    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension == "csv":
            data = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            data = pd.read_excel(uploaded_file)
        elif file_extension == "json":
            data = pd.read_json(uploaded_file)
        st.write("Data Preview:", data.head())

        if st.button("Analyze Data"):
            analysis_response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Analyze the following data and provide a summary including patterns, relationships, and findings:\n\n{data.head(10)}",
                max_tokens=250
            )
            st.write("Data Analysis Summary:")
            st.write(analysis_response.choices[0].text.strip())

        if st.button("Generate Visualization"):
            fig, ax = plt.subplots()
            data.plot(ax=ax)  # Automatically choose best plot type based on data
            buf = BytesIO()
            plt.savefig(buf, format="png")
            st.image(buf)
