import streamlit as st
import os
import time
from graph import graph

st.set_page_config(page_title="Data Analysis & Visualization Agent", page_icon="📊")

st.title("📊 Data Analysis & Visualization Agent")
st.markdown("Upload a dataset and ask me to analyze it or create visualizations.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Save the file temporarily to pass path to pandas
    dataset_path = f"temp_{uploaded_file.name}"
    with open(dataset_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Loaded {uploaded_file.name}")
    
    query = st.text_input("What would you like to know or plot from this dataset?", placeholder="e.g., Clean the data and plot sales by region.")
    
    if st.button("Analyze"):
        with st.spinner("Analyzing data and generating code..."):
            initial_state = {
                "query": query,
                "dataset_path": dataset_path
            }
            
            # Remove any existing output_plot.png from previous runs
            if os.path.exists("output_plot.png"):
                os.remove("output_plot.png")
            
            # Run the agent graph
            final_state = graph.invoke(initial_state)
            
            st.subheader("Agent Summary")
            st.write(final_state["analysis"])
            
            with st.expander("View generated Python code"):
                st.code(final_state["generated_code"], language="python")
                
            # If the code saved a plot, display it
            if os.path.exists("output_plot.png"):
                st.image("output_plot.png", caption="Generated Plot")
                
else:
    st.info("Please upload a dataset to begin.")
