import os
import re
from PyPDF2 import PdfReader, PdfWriter
import streamlit as st
from config import keywords_dict, stop_keywords, anti_keywords

def find_cover(uploaded_file):
    """
    Extracts and saves the first page of a PDF to a temporary file.

    Parameters:
        uploaded_file: The uploaded PDF file.

    Returns:
        str: Path to the temporary file containing the first page of the PDF.
    """
    section_title = "cover"
    if uploaded_file:
        try:
            # Read the PDF and extract the first page
            pdf_reader = PdfReader(uploaded_file)
            first_page = pdf_reader.pages[0]

            pdf_writer = PdfWriter()
            temp_cover_page_path = os.path.join(f"temp_{section_title}_1.pdf")
            with open(temp_cover_page_path, "wb") as f:
                pdf_writer.add_page(first_page)
                pdf_writer.write(f)

            # Return the path to the temporary file
            return temp_cover_page_path
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")
            return None
    else:
        st.warning("Please upload a PDF on the Home page first.")
        return None


def find_underwriter(uploaded_file):
    """
    Searches for pages in a PDF containing specific keywords for the 'underwriter' section and returns the extracted file path.

    Parameters:
        uploaded_file: The uploaded PDF file.

    Returns:
        str: Path to the temporary file containing the extracted 'underwriter' page(s).
    """
    section_name = "underwriter"

    keyword_sets = keywords_dict.get(section_name, [])
    if not keyword_sets:
        st.error(f"No keywords defined for section: {section_name}")
        return None

    if uploaded_file:
        try:
            pdf_reader = PdfReader(uploaded_file)
            total_pages = len(pdf_reader.pages)
            start_page = total_pages // 3  # Skip the first 1/3 of the PDF
            pages = pdf_reader.pages[start_page:]

            # Loop through the keyword sets
            for keyword_set in keyword_sets:
                for page_num, page in enumerate(pages, start=start_page + 1):
                    text = page.extract_text()
                    
                    # Check if any keyword in the set is found on the page
                    if any(re.search(keyword, text, re.IGNORECASE) for keyword in keyword_set):
                        # Save the matched page to a temporary file
                        pdf_writer = PdfWriter()
                        pdf_writer.add_page(page)

                        temp_page_path = os.path.join(f"temp_{section_name}_{page_num}.pdf")
                        with open(temp_page_path, "wb") as f:
                            pdf_writer.write(f)

                        # Return the path of the extracted page
                        return temp_page_path

            st.warning(f"No pages contain the specified keywords for {section_name}.")
            return None
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")
            return None
    else:
        st.warning("Please upload a PDF on the Home page first.")
        return None

def find_financial(uploaded_file, section_name):
    """
    Extracts and displays sections of a PDF based on keyword matches.

    Parameters:
        uploaded_file: The uploaded PDF file (Streamlit file uploader object).
        section_name: The name of the section to search for (e.g., "income_statement").

    Returns:
        bool: True if processing completed without interruptions; False if stopped or an error occurred.
    """
    if uploaded_file:
        try:
            pdf_reader = PdfReader(uploaded_file)
            total_pages = len(pdf_reader.pages)

            # Step 1: Start from the second half of the PDF
            start_page = total_pages // 2
            pages = pdf_reader.pages[start_page:]

            section_keywords = keywords_dict.get(section_name, [])
            section_stop_keywords = stop_keywords.get(section_name, [])
            section_anti_keywords = anti_keywords.get(section_name, [])

            pdf_writer = PdfWriter()  # Writer for the extracted pages
            extraction_started = False  # Flag to check if extraction has started
            extraction_start_page = None  # Track the starting page number
            pages_extracted = 0  # Counter for extracted pages

            for page_num, page in enumerate(pages, start=start_page + 1):
                text = page.extract_text()

                # Step 2: Find the keywords within the keywords_dict
                if not extraction_started:
                    for keyword_set in section_keywords:
                        if all(re.search(keyword, text, re.IGNORECASE) for keyword in keyword_set):
                            pdf_writer.add_page(page)
                            pages_extracted += 1
                            extraction_start_page = page_num  # Set the starting page number

                            # Check for stop keywords on the same page
                            if any(all(re.search(keyword, text, re.IGNORECASE) for keyword in stop_set)
                                   for stop_set in section_stop_keywords):

                                # Check for anti-keywords before stopping
                                if any(all(re.search(keyword, text, re.IGNORECASE) for keyword in anti_set)
                                       for anti_set in section_anti_keywords):
                                    pdf_writer.pages.pop()  # Remove the last added page
                                    pages_extracted -= 1

                                # Save and display the extracted pages (if any)
                                if len(pdf_writer.pages) > 0:
                                    temp_section_path = os.path.join(f"temp_{section_name}_{extraction_start_page}-{page_num}.pdf")
                                    with open(temp_section_path, "wb") as f:
                                        pdf_writer.write(f)
                                    return temp_section_path
                                else:
                                    st.warning(f"No pages matched the criteria for {section_name}.")

                                # Stop extraction immediately and signal to stop all processing
                                return False
                            else:
                                # Continue extraction
                                extraction_started = True
                                break
                elif extraction_started:
                    # Check if we've reached the 3-page limit
                    if pages_extracted >= 3:
                        if len(pdf_writer.pages) > 0:
                            temp_section_path = os.path.join(f"temp_{section_name}_{extraction_start_page}-{page_num-1}.pdf")
                            with open(temp_section_path, "wb") as f:
                                pdf_writer.write(f)
                            return temp_section_path
                        return False

                    # Step 3: Add the page to the output
                    pdf_writer.add_page(page)
                    pages_extracted += 1

                    # Step 4: Check for stop keywords
                    if any(all(re.search(keyword, text, re.IGNORECASE) for keyword in stop_set)
                           for stop_set in section_stop_keywords):

                        # Step 5: After stopping, check for anti-keywords
                        if any(all(re.search(keyword, text, re.IGNORECASE) for keyword in anti_set)
                               for anti_set in section_anti_keywords):
                            pdf_writer.pages.pop()  # Remove the last added page
                            pages_extracted -= 1

                        # Save and display the extracted pages (if any)
                        if len(pdf_writer.pages) > 0:
                            temp_section_path = os.path.join(f"temp_{section_name}_{extraction_start_page}-{page_num}.pdf")
                            with open(temp_section_path, "wb") as f:
                                pdf_writer.write(f)
                            return temp_section_path
                        else:
                            st.warning(f"No pages matched the criteria for {section_name}.")

                        # Stop extraction and signal to stop all processing
                        return False

            # If extraction finished without hitting stop keywords, save and display the pages
            if len(pdf_writer.pages) > 0:
                temp_section_path = os.path.join(f"temp_{section_name}_{extraction_start_page}-{page_num}.pdf")
                with open(temp_section_path, "wb") as f:
                    pdf_writer.write(f)
                return temp_section_path
            else:
                st.warning(f"No pages matched the criteria for {section_name}.")

            # Indicate that processing can continue
            return True

        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")
            # Stop processing due to an error
            return False
    else:
        st.warning("Please upload a PDF on the Home page first.")
        # Stop processing since no file is uploaded
        return False