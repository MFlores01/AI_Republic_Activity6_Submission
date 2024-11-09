import streamlit as st
import openai


def app():
    # Display a header and brief description of Gilgamesh's role
    # Translucent background with title and description
    st.markdown(
        """
        <div style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; text-align: center;'>
            <h1 style='color: #FAFAF0; text-align: left;'>Talk to Gilgamesh!</h1>
            <p style='color: #FAFAF0; text-align: left;'>
                Gilgamesh is a friendly and highly knowledgeable scientist researcher with expertise in Data Science, Computer Science, Linguistics, Social Science, Mathematics, and other fields. Here to guide you through every stage of your research paper.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Define the comprehensive system prompt for Gilgamesh
    system_prompt = """
    You are Gilgamesh, a friendly and highly knowledgeable scientist researcher with a PhD in fields spanning Data Science, Computer Science, Linguistics, Social Science, Mathematics, Biology, Medical Technology, Optometry, Pharmacy, Computer Engineering, Information Technology, Artificial Intelligence, Data Analytics, and more. Your purpose is to guide students through the process of creating high-quality, unique research papers at every stage.

    Gilgamesh provides factual information and tailored, specific examples for each section of the paper, based on the student's topic. Additionally, Gilgamesh can create and suggest visualizations (graphs, charts, diagrams, etc.) that enhance data presentation and interpretation, making research findings clear and impactful.

    Key Responsibilities:
    - Provide tailored, step-by-step guidance with specific examples for each section of a research paper.
    - Identify research gaps and suggest appropriate methodologies.
    - Design relevant visualizations to enhance data presentation.

    Each response should be clear, concise, and factual, with specific examples when applicable.
    """

    # Add a dropdown for the user to select which section they need help with
    section = st.selectbox("Select Section to Discuss", [
        "Introduction",
        "Background of Study",
        "Scope and Limitation",
        "Significance of Study",
        "Conceptual Framework",
        "Literature Review",
        "Methodology"
    ])

    # Text area for user's specific question or needs
    user_input = st.text_area("Describe your needs or questions for this section:", key="user_input")

    # "Send" button to generate the chat response
    if st.button("Send"):
        # Only proceed if there is user input
        if user_input:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Help the student with the {section} of their paper: {user_input}"}
                ],
                max_tokens=1000
            )

            # Display the response as a conversational answer from Gilgamesh
            st.subheader(f"Gilgamesh's Guidance on {section}:")
            st.write(response.choices[0].message['content'])  # No strip to preserve formatting
        else:
            st.warning("Please enter your question or description for Gilgamesh.")

    # Optional: Button for generating a conceptual framework image if that section is selected
    if section == "Conceptual Framework":
        st.image("/path/to/generated_conceptual_framework.png")  # Placeholder path for conceptual framework image
