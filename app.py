import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# App title
st.title("Dataset Visualization App")
st.write("Choose from pre-existing datasets and explore insights through visualizations.")

# Step 1: Predefined Dataset Options
datasets = {
    "Employee Data": "Employee_Data.csv",  # Ensure this file is in the same directory
}

# Step 2: Select Dataset
dataset_name = st.selectbox("Select a Dataset", list(datasets.keys()))
selected_dataset_path = datasets[dataset_name]

# Step 3: Load the Selected Dataset
try:
    df = pd.read_csv(selected_dataset_path)
    st.write("### Dataset Preview")
    st.dataframe(df)
except FileNotFoundError:
    st.error(f"The file '{selected_dataset_path}' was not found. Please ensure it is uploaded.")

# Step 4: Column Selection
st.write("### Select Columns for Analysis")
columns = st.multiselect("Choose one or more columns", df.columns)

# Initialize LabelEncoder for encoding categorical data
label_encoders = {}

if columns:
    st.write("### Selected Columns Data")
    st.dataframe(df[columns])

    # Step 5: Visualization Options
    st.write("### Choose a Visualization Type")
    chart_type = st.radio(
        "Select Chart Type:",
        ('Bar Chart', 'Pie Chart', 'Line Graph')
    )

    # Process each selected column
    for column in columns:
        st.write(f"## Analysis for Column: {column}")

        # Handle Categorical Data by Encoding
        if df[column].dtype == 'object':  # Categorical data
            st.write(f"### Categorical Data: {column}")
            
            # Encode categorical data into numeric values
            label_encoders[column] = LabelEncoder()
            df[column + "_encoded"] = label_encoders[column].fit_transform(df[column])
            encoded_column = column + "_encoded"
            
            st.write(f"Encoded Values for {column}:")
            st.write(df[[column, encoded_column]].drop_duplicates())

            value_counts = df[column].value_counts()

            if chart_type == 'Bar Chart':
                st.write(f"### Bar Chart for {column}")
                fig, ax = plt.subplots()
                ax.bar(value_counts.index, value_counts.values)
                plt.xticks(rotation=45)
                st.pyplot(fig)

            elif chart_type == 'Pie Chart':
                st.write(f"### Pie Chart for {column}")
                fig, ax = plt.subplots()
                ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
                st.pyplot(fig)

            elif chart_type == 'Line Graph':
                st.write(f"### Line Graph for Encoded {column}")
                fig, ax = plt.subplots()
                ax.plot(df[encoded_column].reset_index(drop=True), marker='o', linestyle='-', color='b')
                ax.set_title(f"Line Graph of Encoded {column}")
                ax.set_ylabel("Encoded Values")
                ax.set_xlabel("Index")
                st.pyplot(fig)

        # Handle Numeric Data
        elif pd.api.types.is_numeric_dtype(df[column]):  # Numeric data
            st.write(f"### Numeric Data: {column}")
            
            if chart_type == 'Bar Chart':
                st.write(f"### Bar Chart for {column}")
                value_counts = df[column].value_counts()
                fig, ax = plt.subplots()
                ax.bar(value_counts.index, value_counts.values)
                plt.xticks(rotation=45)
                st.pyplot(fig)

            elif chart_type == 'Pie Chart':
                st.write(f"### Pie Chart for {column}")
                value_counts = df[column].value_counts()
                fig, ax = plt.subplots()
                ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
                st.pyplot(fig)

            elif chart_type == 'Line Graph':
                st.write(f"### Line Graph for {column}")
                fig, ax = plt.subplots()
                ax.plot(df[column].reset_index(drop=True), marker='o', linestyle='-', color='b')
                ax.set_title(f"Line Graph of {column}")
                ax.set_ylabel(column)
                ax.set_xlabel("Index")
                st.pyplot(fig)

        else:
            st.warning(f"Column {column} cannot be visualized with the selected options.")
else:
    st.write("Select at least one column to analyze.")
