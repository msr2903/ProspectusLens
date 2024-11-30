import streamlit as st
from section_extract import find_cover, find_underwriter, find_financial
from streamlit_pdf_viewer import pdf_viewer

def process_sections():
    if "processing" not in st.session_state or st.session_state.get("all_processed", False):
        return

    # Only process the current page if it's set and not processed
    current_page = st.session_state.get("current_page")
    current_page_needs_processing = False
    
    if current_page and not st.session_state.get(current_page, None):
        if not st.session_state["processing"].get(current_page, False):
            current_page_needs_processing = True
            key = current_page
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
            st.session_state["processing"][key] = True
            st.rerun()

    # Process remaining sections if not processing current page and not locked
    if not current_page_needs_processing and not st.session_state.get("processing_lock", False):
        sections_to_process = [
            ("cover_path", lambda: find_cover(st.session_state["uploaded_file"])),
            ("underwriter_path", lambda: find_underwriter(st.session_state["uploaded_file"])),
            ("income_statement_path", lambda: find_financial(st.session_state["uploaded_file"], "income_statement")),
            ("balance_sheet_path", lambda: find_financial(st.session_state["uploaded_file"], "balance_sheet")),
            ("cash_flow_path", lambda: find_financial(st.session_state["uploaded_file"], "cash_flow"))
        ]
        
        # Store the section being processed
        if "processing_section" not in st.session_state:
            st.session_state["processing_section"] = None
            
        for key, process_func in sections_to_process:
            if not st.session_state["processing"].get(key, False):
                # Check if we've switched pages during processing
                if (st.session_state.get("processing_section") is not None and 
                    st.session_state["processing_section"] != current_page):
                    st.session_state["processing_section"] = None
                    return  # Stop processing if we've switched pages
                
                st.session_state["processing_section"] = key
                st.session_state[key] = process_func()
                st.session_state["processing"][key] = True
                st.session_state["processing_section"] = None
                
                if not st.session_state.get("all_processed", False):
                    st.rerun()  # Trigger another run to process next section
                break

    # Check if all sections are processed
    st.session_state["all_processed"] = all(st.session_state["processing"].values())

def show_section(section_key):
    """Display the section if available, otherwise inform the user."""
    # Check if we're switching to a different page
    if st.session_state.get("current_page") != section_key:
        # Reset processing state when switching pages
        st.session_state["processing_lock"] = True
        st.session_state["processing_section"] = None
    
    # Update current page
    st.session_state["current_page"] = section_key
    
    temp_path = st.session_state.get(section_key)
    if temp_path:
        # If we have the section, allow background processing of other sections
        st.session_state["processing_lock"] = False
        pdf_viewer(temp_path)
        # Continue processing remaining sections
        if not st.session_state.get("all_processed", False):
            process_sections()
    else:
        # Lock processing and process this section first
        st.session_state["processing_lock"] = True
        if not st.session_state["processing"].get(section_key, False):
            st.info(f"Processing {section_key.replace('_path', '').replace('_', ' ').title()}...")
            process_sections()
        else:
            st.warning(f"Could not process {section_key.replace('_path', '').replace('_', ' ')}.")
