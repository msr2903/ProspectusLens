import streamlit as st
from sidebar import uploader_sidebar
from section_handlers import show_section

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