import streamlit as st
import openai

def app():
    st.title("Title Generation & Scrutiny")

    user_input = st.text_input("Describe your topic or keywords for title suggestions:")

    if user_input:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Generate unique, novel research titles on the topic: {user_input}. Provide a brief justification for each title’s choice.",
            max_tokens=150
        )
        titles = response.choices[0].text.strip().split('\n')

        st.subheader("Suggested Titles:")
        for i, title in enumerate(titles):
            st.write(f"{i+1}. {title}")

        selected_title = st.selectbox("Select a title for further scrutiny", titles)

        if selected_title:
            scrutiny_response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Provide an in-depth scrutiny of the title '{selected_title}', including relevance, novelty, and anticipated defense questions.",
                max_tokens=200
            )
            st.subheader("Scrutiny and Justification:")
            st.write(scrutiny_response.choices[0].text.strip())
