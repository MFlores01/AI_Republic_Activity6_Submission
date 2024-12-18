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

# Main app logic for defense preparation
def app():
    # Ensure defense_prep_messages is initialized in session state
    if "defense_prep_messages" not in st.session_state:
        st.session_state.defense_prep_messages = []

    # File upload for defense preparation
    uploaded_file = st.file_uploader("Upload your thesis/proposal document (Text files only):", type=["txt", "docx", "pdf"])

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
                 messages=[{"role": "system", "content": """
                Role: You are a research assistant for thesis or research defense preparation.

                Instruction: Provide feedback, suggestions, and answers to questions directly related to the user’s research paper, including clarifications, critiques, defense preparation tips, or questions that may be asked during a defense.

                Constraint: Limit responses to topics relevant to the document's content, research methodology, findings, and defense preparation. Avoid generating unrelated code snippets, general development queries, or questions outside the scope of research. If unsure, request the user to clarify how the question relates to their thesis or defense.
                Do not entertain questions unrelated to research.
                Criteria: Ensure responses are concise, relevant to the research context, and academically supportive. Avoid general advice that isn’t specific to the document’s content.

                Examples:
                - If asked, "Can you generate a web app for this?", respond: "Sorry I can only entertain with research-focused questions."
                - If asked, "What are potential questions on my methodology?", provide relevant questions that probe methodology validity and alignment.
                - If asked, "Summarize findings", summarize main conclusions drawn from the document, noting any insights or implications.
                """},
                {"role": "user", "content": f"Review the following thesis document and provide comprehensive feedback for a defense preparation, including potential questions and critique points:\n\n{text_content[:1000]}"}
            ],
            max_tokens=900
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
        with st.chat_message("user", avatar="images/User.jpg"):
            st.markdown(prompt)

        # Get response from OpenAI
        with st.chat_message("assistant", avatar="images/Gilgamesh.jpg"):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                {"role": "system", "content": """
                Role: You are a research assistant for thesis or research defense preparation.

                Instruction: Provide feedback, suggestions, and answers to questions directly related to the user’s research paper, including clarifications, critiques, defense preparation tips, or questions that may be asked during a defense.

                Constraint: Limit responses to topics relevant to the document's content, research methodology, findings, and defense preparation. Avoid generating unrelated code snippets, general development queries, or questions outside the scope of research. If unsure, request the user to clarify how the question relates to their thesis or defense.
                Do not enter
                Criteria: Ensure responses are concise, relevant to the research context, and academically supportive. Avoid general advice that isn’t specific to the document’s content.

                Examples:
                - If asked, "Can you generate a web app for this?", respond: "Sorry I can only entertain with research-focused questions."
                - If asked, "What are potential questions on my methodology?", provide relevant questions that probe methodology validity and alignment.
                - If asked, "Summarize findings", summarize main conclusions drawn from the document, noting any insights or implications.
                """}
            ] + st.session_state.defense_prep_messages,
            max_tokens=900,
            temperature=1.0
            )
            reply = response.choices[0].message['content']
            st.markdown(reply)

        # Add assistant's response to chat history
        st.session_state.defense_prep_messages.append({"role": "assistant", "content": reply})

# Uncomment this line to run the app directly if needed
# app()
