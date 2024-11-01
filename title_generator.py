import streamlit as st
import openai
import re


def app():

    user_input = st.text_input("Describe your topic or keywords for title suggestions:")

    if user_input:
        # Request the AI to generate titles and justifications
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a research assistant helping generate research titles."},
                {"role": "user",
                 "content": f"Generate 5 unique, novel research titles on the topic: {user_input}. Provide a brief justification for each title’s choice."}
            ],
            max_tokens=500
        )

        # Extract response content without stripping
        content = response.choices[0].message['content']

        # Print raw content for debugging
        st.write("### Suggested Titles:")
        st.write(content)

        # Use regex to match titles and justifications
        pattern = r'^\d+\.\s+"(.+?)"\s*\n\s*Justification:\s*(.+?)(?=(?:\d+\.\s+")|$)'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

        # Limit to 5 titles
        titles = matches[:5]

        # Display the titles with justifications
        #st.subheader("Suggested Titles:")
        if titles:
            for i, (title, justification) in enumerate(titles, start=1):
                st.write(f"{i}. {title}")
                st.write(f"    Justification: {justification}")

