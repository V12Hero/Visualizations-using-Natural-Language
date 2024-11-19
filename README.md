# CSV File Analysis and Visualization Application

## Overview

This application provides an intuitive interface for users to upload CSV files, analyze datasets, and generate insights through visualizations—all without requiring any coding expertise. By leveraging advanced data processing and natural language understanding capabilities, the application empowers users to explore their data, define goals, and create compelling visuals effortlessly.

---

## Features

### 1. **Upload and Customize CSV Data**
- **File Upload**: Users can upload CSV files from their local machine.
- **Custom Delimiters**: Choose the appropriate delimiter for your file (e.g., `,`, `;`, `|`).
- **Dynamic Data Parsing**: Automatically detects column names, data types, and other key properties.

---

### 2. **Dataset Summary**
- **Automatic Summarization**: Generates a detailed JSON summary of the dataset, including:
  - Dataset Name
  - Dataset Description
  - Column Names and Descriptions
  - Sample Data Points
  - Statistical Properties (e.g., mean, median, mode, etc.).
- Provides a clear and comprehensive understanding of the dataset’s structure.

---

### 3. **Goal Generation**
- **Interactive Goal Setting**: Click the "Generate Goals" button to create 5 tailored goals based on the dataset.
- Each goal includes:
  - **Question**: What insight is being sought?
  - **Visualization Type**: Suggested visual (e.g., bar chart, pie chart, line graph).
  - **Rationale**: Why this visualization is relevant to the dataset.

---

### 4. **Visual Generation**
- **Data-Driven Visuals**: Use the generated goals to create beautiful, meaningful visualizations directly from the dataset.

---

### 5. **Natural Language Querying**
- **Query Support**: Ask questions about the dataset in plain English.
  - Example: *"Show me the sales trend over the last 6 months."*
- **AI-Powered Visualization**: Translates queries into corresponding visualizations without requiring any coding.

---

## How It Works

1. **Upload**: Import your CSV file and select the delimiter.
2. **Generate Summary**: View a comprehensive JSON summary of the dataset.
3. **Set Goals**: Automatically create 5 actionable goals based on the dataset’s properties.
4. **Create Visuals**: Generate visuals for the defined goals or query the dataset using natural language.
5. **Iterate and Analyze**: Explore your data, query your data, and extract meaningful insights.

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mohit-Agarwal-17/Visualizations-using-Natural-Language.git
   cd Visualizations-using-Natural-Language
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   cd app
   streamlit run nl_Visuals.py
   ```

4. **Access the App**:
   Open your browser and navigate to `http://localhost:8501`.

---

Enjoy exploring your data effortlessly! 🎉