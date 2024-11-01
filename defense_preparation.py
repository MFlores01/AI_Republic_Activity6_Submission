import streamlit as st
import openai

def app():

    uploaded_file = st.file_uploader("Upload your thesis/proposal document (Text files only):", type=["txt", "docx", "pdf"])

    if uploaded_file:
        text_content = uploaded_file.read().decode("utf-8")

        analysis_response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a research assistant providing feedback for defense preparation."},
                {"role": "user", "content": f"Review the following thesis document and provide comprehensive feedback for a defense preparation, including potential questions and critique points:\n\n{text_content[:1000]}"}
            ],
            max_tokens=1000
        )
        st.write("Defense Preparation Feedback:")
        st.write(analysis_response.choices[0].message['content'].strip())
