import streamlit as st
from section_extract import find_cover, find_underwriter, find_financial
from streamlit_pdf_viewer import pdf_viewer

def home():
    st.title("Prospectus Lens")
    st.write("Welcome to the Prospectus Lens! Upload the PDF of the prospectus below!")
    uploaded_file = st.file_uploader("Upload your Prospectus File", accept_multiple_files=False, type=["pdf"])
    st.session_state["uploaded_file"] = uploaded_file
    st.caption("Made with ❤️ by @michael_sr24")

def cover():
    temp_cover_page_path = find_cover(uploaded_file=st.session_state.get("uploaded_file"))
    if temp_cover_page_path:
        pdf_viewer(temp_cover_page_path)
    else:
        st.warning("Could not process the PDF file.")

def underwriter():
    temp_page_path = find_underwriter(uploaded_file=st.session_state.get("uploaded_file"))
    if temp_page_path:
        pdf_viewer(temp_page_path)
    else:
        st.warning("Could not extract the underwriter section.")

def income_statement():
    temp_section_path = find_financial(uploaded_file=st.session_state.get("uploaded_file"), section_name="income_statement")
    if temp_section_path:
        pdf_viewer(temp_section_path)
    else:
        st.warning("Could not extract the income statement section.")

def balance_sheet():
    temp_section_path = find_financial(uploaded_file=st.session_state.get("uploaded_file"), section_name="balance_sheet")
    if temp_section_path:
        pdf_viewer(temp_section_path)
    else:
        st.warning("Could not extract the balance sheet section.")

def cash_flow():
    temp_section_path = find_financial(uploaded_file=st.session_state.get("uploaded_file"), section_name="cash_flow")
    if temp_section_path:
        pdf_viewer(temp_section_path)
    else:
        st.warning("Could not extract the cash flow section.")