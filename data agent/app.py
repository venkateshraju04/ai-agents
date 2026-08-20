import streamlit as st
import os
from graph import graph

st.set_page_config(page_title="Data Analysis Agent", page_icon="📈", layout="wide")

# Inject custom CSS for a more premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    .agent-summary {
        background-color: #1e2127;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 AI Data Analyst")
st.markdown("Upload your dataset and ask complex questions. The agent will analyze the data, generate Python code, and produce insights and visualizations.")

# Layout with sidebar for inputs
with st.sidebar:
    st.header("📂 Data Input")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    
    st.markdown("---")
    st.header("🔍 Query")
    query = st.text_area("What do you want to know?", placeholder="e.g. Clean the data and plot total sales by region as a bar chart.", height=150)
    
    analyze_btn = st.button("Run Analysis")

# Main content area
if uploaded_file is not None:
    dataset_path = f"temp_{uploaded_file.name}"
    with open(dataset_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    if analyze_btn and query:
        with st.spinner("🧠 Agent is analyzing the data and generating code..."):
            initial_state = {
                "query": query,
                "dataset_path": dataset_path
            }
            
            if os.path.exists("output_plot.png"):
                os.remove("output_plot.png")
            
            final_state = graph.invoke(initial_state)
            
            st.success("Analysis Complete!")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📝 Agent Summary")
                st.markdown(f"<div class='agent-summary'>{final_state['analysis']}</div>", unsafe_allow_html=True)
                
            with col2:
                if os.path.exists("output_plot.png"):
                    st.subheader("📊 Visualization")
                    st.image("output_plot.png", use_container_width=True)
                else:
                    st.info("No visualization was generated for this query.")
            
            with st.expander("💻 View Generated Python Code"):
                st.code(final_state["generated_code"], language="python")
                
            # Clean up the temporary dataset file so it doesn't clutter the directory
            if os.path.exists(dataset_path):
                os.remove(dataset_path)

    elif not analyze_btn:
        st.info("Dataset loaded! Enter a query in the sidebar and click 'Run Analysis'.")
else:
    # Empty state
    st.info("👈 Please upload a dataset in the sidebar to begin.")
    
    # Show example of what the UI looks like when empty
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        ### Features
        - 🤖 **Automated Code Generation**: Llama writes pandas/matplotlib code.
        - 🛡️ **Safe Execution**: Code is executed locally in a sandbox.
        - 📊 **Dynamic Visualizations**: View generated plots instantly.
        - 📝 **Intelligent Summaries**: Get plain-English explanations of data.
        """)
    with col2:
        st.markdown("""
        ### Example Queries
        - *"Plot the distribution of ages."*
        - *"Calculate the average revenue per product category."*
        - *"Clean missing values and plot a correlation heatmap."*
        """)
