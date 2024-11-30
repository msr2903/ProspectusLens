import streamlit as st
from section_handlers import process_sections

def uploader_sidebar():
    uploaded_file = st.sidebar.file_uploader("Upload your Prospectus File", accept_multiple_files=False, type=["pdf"])
    st.sidebar.caption("Made with ❤️ by @michael_sr24")

    if uploaded_file:
        # Initialize session state for processing flags and paths
        if "uploaded_file" not in st.session_state:
            st.session_state["uploaded_file"] = uploaded_file
            st.session_state["processing"] = {
                "cover_path": False,
                "underwriter_path": False,
                "income_statement_path": False,
                "balance_sheet_path": False,
                "cash_flow_path": False,
            }
            st.session_state["all_processed"] = False
            st.session_state["current_page"] = None
            st.session_state["processing_lock"] = False
        else:
            st.session_state["uploaded_file"] = uploaded_file
        process_sections()
    else:
        # Clear all session state when no file is uploaded
        keys_to_clear = ["uploaded_file", "processing", "all_processed", 
                        "cover_path", "underwriter_path", "income_statement_path", 
                        "balance_sheet_path", "cash_flow_path", "current_page", "processing_lock"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
