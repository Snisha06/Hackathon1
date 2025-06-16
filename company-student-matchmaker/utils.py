# utils.py
import json

def load_data(file_path):
    """Load JSON data from file"""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        st.error(f"❌ Invalid JSON in file: {file_path}")
        return []