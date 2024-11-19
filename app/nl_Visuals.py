import streamlit as st
import pandas as pd
from Summarizer import summarizer
from Visualizer import visualizer
from AgentBuilder import agentBuilder
import io
import base64
from PIL import Image
from langchain_core.messages import AIMessage, HumanMessage
import json
from GoalGenerator import goals_generate

# Configure the app
st.set_page_config(
    page_title="Data Visualisation",
    layout="wide"
)

# Sidebar for file upload
st.sidebar.title("Upload CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Add an option to select the delimiter
delimiter = st.sidebar.selectbox(
    "Select the delimiter",
    options=[",", ";", "|", "\t"],
    index=0,  # Default to comma
    help="Choose the delimiter used in your CSV file."
)

# Main screen for chatbot-style interface
st.title("Chatbot & CSV Viewer")

# Initialize session state for chat history if not already initialized
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'goals' not in st.session_state:
    st.session_state.goals = None
    st.session_state.goals_error = None

# Initialize session state for other variables
if "summary" not in st.session_state:
    st.session_state.summary = None
    st.session_state.summary_error = None
if "graph" not in st.session_state:
    st.session_state.graph = None
    st.session_state.graph_error = None

if uploaded_file is not None:
    # Read the uploaded file with the chosen delimiter
    try:
        df = pd.read_csv(uploaded_file, delimiter=delimiter)
    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")
        df = None

    if df is not None:
        # Display the first few rows of the dataframe
        st.subheader("Data Preview")
        st.write(df.head())

        # Button to generate summary
        if st.button("Generate Summary"):
            try:
                # Generate summary

                # summary_result = json.loads(json_data)
                summary_result = summarizer(df)
                
                # Validate if the result is JSON
                if isinstance(summary_result, dict):  # Check if it's a dictionary (JSON-like structure)
                    st.session_state.summary = summary_result
                    st.session_state.summary_error = None  # Clear previous errors
                else:
                    raise ValueError("Generated summary is not a valid JSON object.")
            
            except Exception as e:
                # Handle errors during summary generation or validation
                st.session_state.summary_error = str(e)
                st.session_state.summary = None

        # Display summary or error
        st.subheader("Summary of Data")
        if st.session_state.summary is not None:
            # Add an expander to minimize or expand the summary
            with st.expander("Summary", expanded=True):
                st.json(st.session_state.summary)

        elif st.session_state.summary_error is not None:
            st.error(f"Error generating summary: {st.session_state.summary_error}")
        
        # Generate graph if summary exists
        if st.session_state.summary is not None:
            if st.button("Generate Goals"):
                try:
                    
                    # goals = json.loads(goals_json)
                    goals = goals_generate(st.session_state.summary)
                   
                    if isinstance(goals, list):
                        st.session_state.goals = goals
                        st.session_state.goals_error = None
                        # print(goals)
                    else:
                        raise ValueError("Generated goals is not a valid JSON object.")
                except Exception as e:
                    st.session_state.goals_error = str(e)
                    st.session_state.goals = None

            if st.session_state.graph is None:  # Check if graph is already in session state
                try:
                    st.session_state.graph = agentBuilder(df, st.session_state.summary)
                    st.session_state.graph_error = None  # Clear previous errors
                except Exception as e:
                    st.session_state.graph_error = str(e)
                    st.session_state.graph = None
            
            if st.session_state.graph_error:
                st.error(f"Error generating graph: {st.session_state.graph_error}")
            else:

                if st.session_state.goals is not None:
                    with st.expander("Goals", expanded=True):
                        st.json(st.session_state.goals)
                    if st.button("Use Goals"):
                        for goal in st.session_state.goals:
                            print(goal['question'])
                            _, goal_visual, goal_code = visualizer(
                                st.session_state.graph, df, st.session_state.summary, goal['question']
                            )
                            
                            goal_image_data = base64.b64decode(goal_visual)
                            goal_image = Image.open(io.BytesIO(goal_image_data))
                            st.session_state.chat_history.append(HumanMessage(goal['question']))
                            st.session_state.chat_history.append(goal_image)
                            st.session_state.chat_history.append(AIMessage(goal['rationale']))
                            st.session_state.chat_history.append(goal_code)

                # Chatbot-style interaction
                st.subheader("Chatbot Interface")
                user_input = st.chat_input("Enter your query:")
                if user_input:
                    # Add the user input to the chat history
                    st.session_state.chat_history.append(HumanMessage(user_input))
                    try:
                        # Generate response from visualizer function
                        summ, visual, code = visualizer(
                            st.session_state.graph, df, st.session_state.summary, user_input
                        )

                        # Display the image
                        image_data = base64.b64decode(visual)
                        image = Image.open(io.BytesIO(image_data))

                        # Append the bot response (image, summary, code) to chat history
                        st.session_state.chat_history.append(image)
                        st.session_state.chat_history.append(AIMessage(summ))
                        st.session_state.chat_history.append(code)

                    except Exception as e:
                        st.session_state.chat_history.append(f"Error processing query: {str(e)}")
                    
                # Display chat history
                for message in st.session_state.chat_history:
                    if isinstance(message, HumanMessage):
                        with st.chat_message("Human"):
                            st.write(message.content)
                    elif isinstance(message, Image.Image):
                        with st.chat_message("AI"):
                            st.image(message)
                    elif isinstance(message, AIMessage):
                        with st.chat_message("AI"):
                            with st.expander("Visualization Summary", expanded=False):
                                st.write(message.content)
                    elif isinstance(message, str):
                        with st.chat_message("AI"):
                            with st.expander("Code", expanded=False):
                                st.code(message)
                        
                        
else:
    st.write("Please upload a CSV file to get started.")
