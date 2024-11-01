import streamlit as st
import openai
import re

def app():
    user_input = st.text_input("Describe your topic or keywords for title suggestions:")

    # Create a button to send the title generation request
    if st.button("Send Title"):
        if user_input:
            # Request the AI to generate titles and justifications
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a research assistant helping generate research titles."},
                    {"role": "user",
                     "content": f"Generate 5 unique, novel research titles on the topic: {user_input}. For each title, provide a brief justification, an explanation of key concepts, and potential scrutinization points that could be raised during a research title defense."}
                ],
                max_tokens=1000
            )

            # Extract response content
            content = response.choices[0].message['content']

            # Display raw content for debugging
            st.write("### Suggested Titles:")
            st.write(content)

            # Use regex to match titles, justifications, explanations, and scrutinization points
            pattern = r'^\d+\.\s+"(.+?)"\s*\n\s*Justification:\s*(.+?)\s*Explanation:\s*(.+?)\s*Scrutinization:\s*(.+?)(?=(?:\d+\.\s+")|$)'
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

            # Limit to 5 titles
            titles = matches[:5]

            # Display the titles with justifications, explanations, and scrutinization
            if titles:
                for i, (title, justification, explanation, scrutinization) in enumerate(titles, start=1):
                    st.write(f"**{i}. {title}**")
                    st.write(f"**Justification:** {justification}")
                    st.write(f"**Explanation:** {explanation}")
                    st.write(f"**Scrutinization Points:** {scrutinization}")
                    st.write("---")
        else:
            st.warning("Please enter a topic or keywords before clicking 'Send Title'.")
