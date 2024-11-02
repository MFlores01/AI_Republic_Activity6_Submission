import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import openai

# Define system prompt for Casein Nitrate
system_prompt = """
You are Casein Nitrate, an expert in data analysis and visualization. You assist users with various types of data visualizations, providing guidance on the best charts to use, generating example charts, and offering code samples if requested. You adapt explanations based on the user’s level of experience, ensuring that all responses are informative and educational. Maintain a professional and friendly tone throughout.

Instructions:
- Determine the best chart type based on the user's input or dataset characteristics (such as bar, line, scatter, or more advanced visualizations).
- Offer step-by-step guidance in understanding, creating, and interpreting charts, using practical examples when applicable.
- Provide example code when asked, explaining how each part works.
- Be engaging and supportive, encouraging users to explore different visualization methods to uncover insights in their data.

Constraints:
- Focus on visualizations and avoid unrelated topics.
- Avoid overwhelming users with technical jargon unless they specifically request detailed explanations.
"""

# Initialize conversation history without displaying the system prompt
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting message
    st.session_state.messages.append({"role": "assistant",
                                      "content": "Hi! I'm Casein Nitrate. I'm here to help you with data visualizations and analysis. Ask me about charts, data insights, or code examples!"})

# Store the uploaded data in session state if available
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# Function to suggest chart types based on data structure without forcing a default
def suggest_chart_type(data):
    num_cols = data.select_dtypes(include=np.number).columns
    cat_cols = data.select_dtypes(include="object").columns
    suggestions = []

    # Add appropriate suggestions based on data structure
    if len(num_cols) > 1:
        suggestions.append("pair plot")  # Multiple numeric columns
        suggestions.append("correlation heatmap")  # For examining correlations

    if len(num_cols) >= 1:
        suggestions.append("histogram")  # Suitable for distribution of single numerical column
        if len(num_cols) == 2:
            suggestions.append("scatter plot")  # Two numerical columns

    if len(cat_cols) >= 1 and len(num_cols) >= 1:
        suggestions.append("bar plot")  # Categorical + numerical

    if len(cat_cols) == 1 and len(num_cols) >= 1:
        suggestions.append("box plot")  # Categorical + numerical for distribution

    return suggestions

# Helper function to generate and display a selected chart type
def generate_chart(chart_type, data):
    buf = BytesIO()
    try:
        plt.figure()

        # Define num_cols and cat_cols inside this function
        num_cols = data.select_dtypes(include=np.number).columns
        cat_cols = data.select_dtypes(include="object").columns

        if chart_type == "scatter plot":
            sns.scatterplot(x=num_cols[0], y=num_cols[1], data=data)
            plt.title("Scatter Plot")
        elif chart_type == "line plot":
            plt.plot(data[num_cols[0]], data[num_cols[1]], marker='o')
            plt.title("Line Plot")
        elif chart_type == "bar plot":
            sns.barplot(x=cat_cols[0], y=num_cols[0], data=data)
            plt.title("Bar Plot")
        elif chart_type == "histogram":
            plt.hist(data[num_cols[0]], bins=10)
            plt.title("Histogram")
        elif chart_type == "pair plot":
            sns.pairplot(data.select_dtypes(include=[np.number]))
        elif chart_type == "correlation heatmap":
            corr = data.corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm")
            plt.title("Correlation Heatmap")
        elif chart_type == "box plot":
            sns.boxplot(x=cat_cols[0], y=num_cols[0], data=data)
            plt.title("Box Plot")
        else:
            st.write("Unsupported chart type.")
            return None

        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        return buf
    except Exception as e:
        st.write("Error generating chart:", e)
        return None


# Generate code example based on the chart type
def generate_code_for_chart(chart_type):
    code_template = {
        "line": """
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 11)
y = np.random.randint(1, 20, size=10)

plt.plot(x, y, marker='o')
plt.title("Line Chart Example")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
""",
        "bar": """
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 11)
y = np.random.randint(1, 20, size=10)

plt.bar(x, y)
plt.title("Bar Chart Example")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.show()
""",
        "scatter": """
import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(50)
y = np.random.rand(50)

plt.scatter(x, y)
plt.title("Scatter Plot Example")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
""",
        "histogram": """
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(100)

plt.hist(data, bins=10)
plt.title("Histogram Example")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
"""
    }
    return code_template.get(chart_type, "Unsupported chart type.")

# Determine chart type based on user input using OpenAI API
def determine_chart_type_with_openai(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages + [
            {"role": "user", "content": user_input}],
        max_tokens=500,
        temperature=1
    )
    chart_recommendation = response.choices[0].message['content'].strip().lower()

    if "pair plot" in chart_recommendation:
        return "pair plot"
    elif "correlation heatmap" in chart_recommendation:
        return "correlation heatmap"
    elif "scatter plot" in chart_recommendation:
        return "scatter plot"
    elif "line plot" in chart_recommendation:
        return "line plot"
    elif "bar plot" in chart_recommendation:
        return "bar plot"
    elif "histogram" in chart_recommendation:
        return "histogram"
    elif "box plot" in chart_recommendation:
        return "box plot"
    else:
        return None


# Main app logic
def app():
    st.markdown(
        """
        <div style='background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; text-align: center;'>
            <h1 style='color: #FAFAF0; text-align: left;'>Data Analysis & Visualization</h1>
            <p style='color: #FAFAF0; text-align: left;'>
                Casein Nitrate is here to help you understand your data with analysis and visualizations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    #st.write("Casein Nitrate is here to help you understand your data with analysis and visualizations.")

    # Data file upload
    uploaded_file = st.file_uploader("Upload your data file (CSV, Excel, JSON):", type=["csv", "xlsx", "json"])
    if uploaded_file:
        if uploaded_file.name.endswith("csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith("xlsx"):
            data = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith("json"):
            data = pd.read_json(uploaded_file)
        st.session_state.uploaded_data = data
        st.write("Data Preview:", data.head())

    # Chat input area
    user_input = st.chat_input("Ask Casein Nitrate a question or request a visualization:")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Check if data is uploaded and dynamically include it in OpenAI prompt
        if st.session_state.uploaded_data is not None:
            data_info = f"The dataset has {st.session_state.uploaded_data.shape[0]} rows and {st.session_state.uploaded_data.shape[1]} columns. Here are the columns: {', '.join(st.session_state.uploaded_data.columns)}."
            st.session_state.messages.append({"role": "system", "content": data_info})

            # Check if the user asked for suggestions
            if "suggest" in user_input.lower() or "recommend" in user_input.lower():
                suggestions = suggest_chart_type(st.session_state.uploaded_data)
                if suggestions:
                    reply = "Based on your dataset, here are some suggested visualizations:\n" + "\n".join(suggestions)
                else:
                    reply = "I'm unable to suggest a chart for this dataset structure."

            # Generate chart based on user’s specific request
            elif any(keyword in user_input.lower() for keyword in ["generate", "create", "show", "plot"]):
                chart_type = determine_chart_type_with_openai(user_input)
                if chart_type and chart_type in suggest_chart_type(st.session_state.uploaded_data):
                    chart_image = generate_chart(chart_type, st.session_state.uploaded_data)
                    if chart_image:
                        st.image(chart_image, caption=f"{chart_type.capitalize()} for your data")
                        reply = f"Here is the {chart_type} chart generated based on your data."
                    else:
                        reply = "There was an issue generating the chart. Please try another chart type."
                else:
                    reply = "The chart type requested doesn't match the dataset structure. Please choose from the suggested options."

            else:
                # General response from OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                    max_tokens=500,
                    temperature=0.5
                )
                reply = response.choices[0].message['content'].strip()

        else:
            reply = "Please upload a dataset for me to analyze and suggest visualizations."

        # Append assistant's reply
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display conversation history with custom icons
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            # Use custom icon for the assistant
            with st.chat_message("assistant", avatar="images/Casein_Nitrate.jpg"):
                st.markdown(message["content"])
        else:
            # Use custom icon for the user
            with st.chat_message("user", avatar="images/User.jpg"):
                st.markdown(message["content"])

# Uncomment this line to run the app directly if needed
# app()
