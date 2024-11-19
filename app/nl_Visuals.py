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
                json_data = """
{"dataset_name":"Country Statistics","dataset_description":"This dataset provides a comprehensive overview of various socio-economic and developmental indicators for different countries over a period of time. It includes data on economic performance, demographics, health, education, technology, environment, military expenditure, infrastructure, and governance.","fields":[{"column":"Country","field_description":"Name of the country","dtype":"category","samples":["USA","Russia","Australia"],"num_unique_values":6,"semantic_type":"country"},{"column":"Year","field_description":"The year the data was collected","dtype":"int64","samples":[2008,2016,2000],"num_unique_values":24,"semantic_type":"year"},{"column":"GDP (in Trillions USD)","field_description":"Gross Domestic Product, representing the total economic output of a country, measured in trillions of US dollars.","dtype":"number","std":7.807163108594299,"min":1.27,"max":22.24,"samples":[1.82,2.93,1.35],"num_unique_values":94,"semantic_type":"gdp"},{"column":"GDP per Capita (in USD)","field_description":"Gross Domestic Product per capita, representing the average economic output per person in a country, measured in US dollars.","dtype":"number","std":24438.78637868252,"min":2009.7,"max":68120,"samples":[2037,10400,10461],"num_unique_values":134,"semantic_type":"gdp_per_capita"},{"column":"Inflation Rate (%)","field_description":"The annual percentage change in the consumer price index, reflecting the rate at which prices for goods and services are rising.","dtype":"number","std":1.0679399610884082,"min":1.44,"max":5.04,"samples":[2.23,2.28,1.98],"num_unique_values":85,"semantic_type":"inflation_rate"},{"column":"Population (in Millions)","field_description":"Total population of the country, measured in millions.","dtype":"number","std":600.1697975328195,"min":23.9,"max":1462.31,"samples":[140.36,321.4,146.31],"num_unique_values":132,"semantic_type":"population"},{"column":"Population Growth Rate (%)","field_description":"The annual percentage change in the population of a country.","dtype":"number","std":0.41725570834450687,"min":0.1,"max":1.36,"samples":[0.99,1.35,0.61],"num_unique_values":43,"semantic_type":"population_growth_rate"},{"column":"Urban Population (%)","field_description":"Percentage of the population living in urban areas.","dtype":"number","std":17.862888021083503,"min":33.6,"max":90.04,"samples":[75.63,83,34.09],"num_unique_values":119,"semantic_type":"urban_population"},{"column":"Life Expectancy (Years)","field_description":"The average number of years a newborn is expected to live based on current mortality rates.","dtype":"number","std":5.411696172036126,"min":66.14,"max":87.15,"samples":[81.32,79.18,85.51],"num_unique_values":132,"semantic_type":"life_expectancy"},{"column":"Healthcare Expenditure per Capita (USD)","field_description":"The average amount of money spent on healthcare per person, measured in US dollars.","dtype":"number","std":3914.8465032220874,"min":69.42,"max":11528,"samples":[447.75,4945.2,5124],"num_unique_values":128,"semantic_type":"healthcare_expenditure_per_capita"},{"column":"Doctor-to-Patient Ratio","field_description":"The number of doctors per 1,000 patients.","dtype":"number","std":1.0295199864433922,"min":0.86,"max":4.2,"samples":[2.83,0.87,2.81],"num_unique_values":90,"semantic_type":"doctor_patient_ratio"},{"column":"Literacy Rate (%)","field_description":"The percentage of the population aged 15 and over who can both read and write.","dtype":"number","std":9.655823405394766,"min":70.6,"max":103.95,"samples":[98.7,102.96,101.77],"num_unique_values":100,"semantic_type":"literacy_rate"}]}
"""
                summary_result = json.loads(json_data)
                # summary_result = summarizer(df)
                
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
                    goals_json = """
                    [
                    {
                        "index": 0,
                        "question": "How does GDP per capita correlate with life expectancy across different countries and years?",
                        "visualization": "Scatter plot of 'GDP per Capita (in USD)' vs. 'Life Expectancy (Years)', colored by 'Country' and animated by 'Year'.",
                        "rationale": "This visualization helps explore the relationship between economic prosperity and health outcomes. Coloring by country allows for comparison across different nations, while animating by year reveals trends over time.  We can observe if countries with higher GDP per capita tend to have longer life expectancies and how this relationship evolves over the years."
                    },
                    {
                        "index": 1,
                        "question": "What is the relationship between healthcare expenditure per capita and life expectancy, considering the influence of population density?",
                        "visualization": "Bubble chart with 'Healthcare Expenditure per Capita (USD)' on the x-axis, 'Life Expectancy (Years)' on the y-axis, bubble size representing 'Population (in Millions)', and color representing 'Urban Population (%)'.",
                        "rationale": "This visualization helps analyze the impact of healthcare spending on life expectancy while accounting for population size and urbanization.  By observing the bubble sizes and colors, we can determine if higher healthcare expenditure leads to increased life expectancy and if population density plays a role in this relationship."
                    },
                    {
                        "index": 2,
                        "question": "How does the doctor-to-patient ratio vary across countries with different GDP levels?",
                        "visualization": "Box plot of 'Doctor-to-Patient Ratio' grouped by quantiles of 'GDP (in Trillions USD)'.",
                        "rationale": "This visualization allows for comparing the distribution of doctor-to-patient ratios across different income levels. Grouping countries by GDP quantiles provides a meaningful comparison between wealthier and less wealthy nations. We can determine if there's a significant difference in healthcare access based on a country's economic strength."
                    },
                    {
                        "index": 3,
                        "question": "What is the trend of literacy rates over time for different countries, categorized by their population growth rates?",
                        "visualization": "Line chart of 'Literacy Rate (%)' over 'Year', with separate lines for each 'Country', and color-coded based on quantiles of 'Population Growth Rate (%)'.",
                        "rationale": "This visualization helps analyze the progress of literacy rates over time and investigate the potential influence of population growth on education levels. Grouping countries by population growth rate quantiles allows us to compare countries with similar demographic trends. We can observe if countries with slower population growth tend to have higher literacy rates."
                    },
                    {
                        "index": 4,
                        "question": "How does inflation rate correlate with GDP growth, considering the urban population percentage?",
                        "visualization": "Scatter plot of 'Inflation Rate (%)' vs. the yearly percentage change in 'GDP (in Trillions USD)', with point size representing 'Urban Population (%)'.",
                        "rationale": "This visualization helps understand the relationship between inflation and economic growth, while also considering the impact of urbanization. The size of the points indicates the level of urbanization, which can provide insights into whether urbanization influences the inflation-GDP growth relationship.  We can observe if higher inflation rates are associated with higher or lower GDP growth and if the degree of urbanization has a noticeable effect."
                    }
                    ]

                    """
                    goals = json.loads(goals_json)
                    # goals = goals_generate(st.session_state.summary)
                    if isinstance(goals, list):
                        st.session_state.goals = goals
                        st.session_state.goals_error = None
                        print(goals)
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
