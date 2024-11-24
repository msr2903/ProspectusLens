import streamlit as st
from pages import home, cover, underwriter, income_statement, balance_sheet, cash_flow

# Define pages
pages = {
    "": [
        st.Page(home, title="Home"),
    ],
    "IPO Info:": [
        st.Page(cover, title="Cover"),
        st.Page(underwriter, title="Underwriter")
    ],
    "Financial:": [
        st.Page(income_statement, title="Income Statement"),
        st.Page(balance_sheet, title="Balance Sheet"),
        st.Page(cash_flow, title="Cash Flow")
    ],
}

# Navigation
pg = st.navigation(pages)  # Pass the entire pages dictionary
pg.run()