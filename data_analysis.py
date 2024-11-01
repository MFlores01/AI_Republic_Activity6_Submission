import streamlit as st
import pandas as pd
import openai
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Define the system prompt for Casein Nitrate
system_prompt = """
You are Casein Nitrate, a data analysis and visualization expert chatbot. You are here to help users understand and analyze their datasets, offering summaries, pattern insights, and generating relevant visualizations upon request. You can produce line charts, bar charts, and scatter plots with detailed explanations of each.

### Key Capabilities:
- **Data Analysis Summaries**: Provide summaries, detect patterns, and highlight key relationships in datasets.
- **Chart Creation**: Generate line, bar, and scatter plots with labeled axes and appropriate titles.
- **Chart Recommendations**: Suggest the best types of visualizations based on data characteristics.

### Interaction Guidelines:
- Always ask clarifying questions if the user’s request is ambiguous.
- Generate visualizations using `matplotlib` for clear and insightful data representation.
- Ensure each chart has titles and labels for both axes.
"""


def generate_chart(chart_type, data):
    fig, ax = plt.subplots()
    if chart_type == "line":
        ax.plot(data['x'], data['y'], marker='o')
        ax.set_title("Line Chart Example")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
    elif chart_type == "bar":
        ax.bar(data['x'], data['y'])
        ax.set_title("Bar Chart Example")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Values")
    elif chart_type == "scatter":
        ax.scatter(data['x'], data['y'])
        ax.set_title("Scatter Plot Example")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
    else:
        raise ValueError("Unsupported chart type")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf


def app():
    st.write("Casein Nitrate is here to help you understand your data with analysis and visualizations.")

    uploaded_file = st.file_uploader("Upload your data file (CSV, Excel, JSON, etc.):", type=["csv", "xlsx", "json"])

    if uploaded_file:
        # Load data based on file type
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension == "csv":
            data = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            data = pd.read_excel(uploaded_file)
        elif file_extension == "json":
            data = pd.read_json(uploaded_file)

        st.write("Data Preview:")
        st.write(data.head())

        user_input = st.text_area(
            "Ask Casein Nitrate for insights or request a specific visualization (e.g., 'Generate a bar chart'):")

        if st.button("Send"):
            # Set up the conversation with Casein Nitrate's system prompt
            messages = [{"role": "system", "content": system_prompt}]
            messages.append({"role": "user", "content": user_input})

            # Check if the user requested a specific visualization
            if "visualization" in user_input or "chart" in user_input:
                # Placeholder data for visualization; replace with actual data columns as needed
                sample_data = {
                    'x': np.arange(1, 11),
                    'y': np.random.randint(1, 20, size=10)
                }

                # Determine chart type based on user input
                if "line" in user_input.lower():
                    chart_type = "line"
                elif "bar" in user_input.lower():
                    chart_type = "bar"
                elif "scatter" in user_input.lower():
                    chart_type = "scatter"
                else:
                    chart_type = "line"  # Default to line chart if not specified

                # Generate and display the chart
                chart = generate_chart(chart_type, sample_data)
                st.image(chart, caption=f"{chart_type.capitalize()} Chart Example")

                # Add assistant response about the chart generation
                st.write(f"Casein Nitrate: Here’s a {chart_type} chart based on your request.")
            else:
                # Perform regular chat interaction if no visualization was requested
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=1000
                )
                st.write("Casein Nitrate:", response.choices[0].message['content'])

        if st.button("Analyze Data"):
            analysis_response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",
                     "content": f"Analyze the following data and provide a summary including patterns, relationships, and findings:\n\n{data.head(10)}"}
                ],
                max_tokens=1000
            )
            st.write("Data Analysis Summary:")
            st.write(analysis_response.choices[0].message['content'])

