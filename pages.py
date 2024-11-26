import streamlit as st
from section_extract import find_cover, find_underwriter, find_section

def home():
    st.title("Prospectus Lens")
    st.write("Welcome to the Prospectus Lens! Upload the PDF of the prospectus below!")
    uploaded_file = st.file_uploader("Upload your Prospectus File", accept_multiple_files=False, type=["pdf"])
    st.session_state["uploaded_file"] = uploaded_file
    st.caption("Made with ❤️ by @michael_sr24")

def cover():
    find_cover(uploaded_file=st.session_state.get("uploaded_file"))

def underwriter():
    find_underwriter(
        uploaded_file=st.session_state.get("uploaded_file"),
    )

def income_statement():
    find_section(
        uploaded_file=st.session_state.get("uploaded_file"),
        section_name="income_statement",
    )

def balance_sheet():
    find_section(
        uploaded_file=st.session_state.get("uploaded_file"),
        section_name="balance_sheet",
    )

def cash_flow():
    find_section(
        uploaded_file=st.session_state.get("uploaded_file"),
        section_name="cash_flow",
    )
