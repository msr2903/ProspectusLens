import streamlit as st
from section_extract import find_cover, find_underwriter, find_financial
from streamlit_pdf_viewer import pdf_viewer

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
        else:
            st.session_state["uploaded_file"] = uploaded_file
        process_sections()
    else:
        # Clear all session state when no file is uploaded
        keys_to_clear = ["uploaded_file", "processing", "all_processed", 
                        "cover_path", "underwriter_path", "income_statement_path", 
                        "balance_sheet_path", "cash_flow_path"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

def process_sections():
    if "processing" in st.session_state and not st.session_state.get("all_processed", False):
        for key, processed in st.session_state["processing"].items():
            if not processed:
                if key == "cover_path":
                    st.session_state[key] = find_cover(st.session_state["uploaded_file"])
                elif key == "underwriter_path":
                    st.session_state[key] = find_underwriter(st.session_state["uploaded_file"])
                elif key == "income_statement_path":
                    st.session_state[key] = find_financial(st.session_state["uploaded_file"], "income_statement")
                elif key == "balance_sheet_path":
                    st.session_state[key] = find_financial(st.session_state["uploaded_file"], "balance_sheet")
                elif key == "cash_flow_path":
                    st.session_state[key] = find_financial(st.session_state["uploaded_file"], "cash_flow")

                st.session_state["processing"][key] = True  # Mark as processed
                break

        # Check if all sections are processed
        st.session_state["all_processed"] = all(st.session_state["processing"].values())

def show_section(section_key):
    """Display the section if available, otherwise inform the user."""
    temp_path = st.session_state.get(section_key)
    if temp_path:
        pdf_viewer(temp_path)
    else:
        if not st.session_state["processing"].get(section_key, False):
            st.info(f"{section_key.replace('_', ' ').capitalize()} is still being processed.")
        else:
            st.warning(f"Could not process {section_key.replace('_', ' ')}.")

def home():
    st.title("Prospectus Lens")
    st.write("Welcome to the Prospectus Lens! Upload the PDF of the prospectus on the left sidebar!")

def cover():
    st.title("Cover")
    if "uploaded_file" in st.session_state:
        show_section("cover_path")
    else:
        st.warning("Please upload a file first!")

def underwriter():
    st.title("Underwriter")
    if "uploaded_file" in st.session_state:
        show_section("underwriter_path")
    else:
        st.warning("Please upload a file first!")

def income_statement():
    st.title("Income Statement")
    if "uploaded_file" in st.session_state:
        show_section("income_statement_path")
    else:
        st.warning("Please upload a file first!")

def balance_sheet():
    st.title("Balance Sheet")
    if "uploaded_file" in st.session_state:
        show_section("balance_sheet_path")
    else:
        st.warning("Please upload a file first!")

def cash_flow():
    st.title("Cash Flow")
    if "uploaded_file" in st.session_state:
        show_section("cash_flow_path")
    else:
        st.warning("Please upload a file first!")