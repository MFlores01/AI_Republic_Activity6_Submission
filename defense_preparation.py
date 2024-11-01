import streamlit as st
import openai
from docx import Document
import PyPDF2


# Function to read DOCX file
def read_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


# Function to read PDF file
def read_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = []
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text.append(page.extractText())
    return "\n".join(text)


# Initialize chat session for defense preparation
if "defense_prep_messages" not in st.session_state:
    st.session_state.defense_prep_messages = []


# Main app logic for defense preparation
def app():

    # File upload for defense preparation
    uploaded_file = st.file_uploader("Upload your thesis/proposal document (Text files only):",
                                     type=["txt", "docx", "pdf"])

    # Display feedback if a file is uploaded
    if uploaded_file:
        # Determine file type and read content accordingly
        if uploaded_file.type == "text/plain":
            text_content = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text_content = read_docx(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            text_content = read_pdf(uploaded_file)
        else:
            st.error("Unsupported file format.")
            return

        # Generate initial feedback using OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a research assistant providing feedback for defense preparation."},
                {"role": "user",
                 "content": f"Review the following thesis document and provide comprehensive feedback for a defense preparation, including potential questions and critique points:\n\n{text_content[:1000]}"}
            ],
            max_tokens=700
        )
        feedback = response.choices[0].message['content'].strip()
        st.write("Defense Preparation Feedback:")
        st.write(feedback)

    # Chat interface for additional queries in defense preparation
    st.header("Chat with Gilgamesh - Defense Preparation")

    # Display chat messages from defense preparation history
    for message in st.session_state.defense_prep_messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar="images/Gilgamesh.jpg"):
                st.markdown(message["content"])
        else:
            with st.chat_message("user", avatar="images/User.jpg"):
                st.markdown(message["content"])

    # Accept user input for chat
    if prompt := st.chat_input("Ask Gilgamesh a question about your defense preparation or request additional help"):
        # Add user message to chat history
        st.session_state.defense_prep_messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from OpenAI
        with st.chat_message("assistant"):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system",
                           "content": "You are a helpful research assistant for defense preparation."}] + st.session_state.defense_prep_messages,
                max_tokens=700,
                temperature=1.0
            )
            reply = response.choices[0].message['content']
            st.markdown(reply)

        # Add assistant's response to chat history
        st.session_state.defense_prep_messages.append({"role": "assistant", "content": reply})
