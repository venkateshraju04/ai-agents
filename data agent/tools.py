import sys
from io import StringIO
import traceback

def execute_python(code: str, dataset_path: str) -> str:
    """
    Executes the given Python code. 
    The code should assume `df` is already loaded via pandas, but to make it self-contained, 
    we inject the df loading.
    Returns the standard output or error.
    """
    # Create a wrapper that captures stdout
    setup_code = f"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import sys

# Load the dataset
try:
    if '{dataset_path}'.endswith('.csv'):
        df = pd.read_csv('{dataset_path}')
    elif '{dataset_path}'.endswith('.xlsx'):
        df = pd.read_excel('{dataset_path}')
    else:
        df = pd.read_csv('{dataset_path}') # fallback
except Exception as e:
    print(f"Error loading dataset: {{e}}")
"""
    
    full_code = setup_code + "\n" + code

    # Redirect stdout to capture prints
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        # We use a restricted dictionary for local variables
        local_vars = {}
        exec(full_code, globals(), local_vars)
        output = redirected_output.getvalue()
        if not output:
            output = "Code executed successfully with no output."
    except Exception as e:
        output = f"Error executing code:\n{traceback.format_exc()}"
    finally:
        sys.stdout = old_stdout

    return output
