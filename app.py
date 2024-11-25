import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App title
st.title("Dataset Visualization App")
st.write("Choose from pre-existing datasets and explore insights through visualizations.")

# Step 1: Predefined Dataset Options
datasets = {
    "Employee Data":"Employee_Data.csv",
}

# Step 2: Select Dataset
dataset_name = st.selectbox("Select a Dataset", list(datasets.keys()))
selected_dataset_path = datasets[dataset_name]

# Step 3: Load the Selected Dataset
df = pd.read_csv(selected_dataset_path)
st.write("### Dataset Preview")
st.dataframe(df)

# Step 4: Visualization Options
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
st.write("### Select Columns for Visualization")
if len(numeric_columns) > 0:
    column = st.selectbox("Choose a column", numeric_columns)

    st.write("### Choose a Visualization Type")
    chart_type = st.radio(
        "Select Chart Type:",
        ('Pie Chart', 'Bar Chart', 'Line Graph')
    )

    # Generate and Display Chart
    if chart_type == 'Pie Chart':
        st.write(f"### Pie Chart for {column}")
        pie_data = df[column].value_counts()
        fig, ax = plt.subplots()
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        st.pyplot(fig)

    elif chart_type == 'Bar Chart':
        st.write(f"### Bar Chart for {column}")
        bar_data = df[column].value_counts()
        fig, ax = plt.subplots()
        ax.bar(bar_data.index, bar_data.values)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif chart_type == 'Line Graph':
        st.write(f"### Line Graph for {column}")
        fig, ax = plt.subplots()
        ax.plot(df[column])
        st.pyplot(fig)
else:
    st.write("No numeric columns available for visualization.")
