"""
AI-Powered Radiology Report Generator

This application uses AI to generate comprehensive radiology reports from chest X-ray images.
"""

import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

# Import application modules
from app.constants import ERROR_API_KEY_MISSING
from app.config_manager import config_manager
from app.api import api_client
from app.styles import get_css, get_app_header_html, get_app_description_html
from app.ui_components import (render_sidebar, render_image_upload,
                               render_clinical_form, validate_inputs, display_report)

# Load environment variables
load_dotenv()


def main():
    """Main application entry point."""
    # Configure the Streamlit page
    st.set_page_config(**config_manager.get_page_config())

    # Apply custom CSS
    st.markdown(get_css(), unsafe_allow_html=True)

    # Display application header
    st.markdown(get_app_header_html(), unsafe_allow_html=True)

    # Display application description
    st.markdown(get_app_description_html(), unsafe_allow_html=True)

    # Check for API key
    if not api_client.is_configured():
        st.error(ERROR_API_KEY_MISSING)
        return

    # Render sidebar with patient information
    patient_info = render_sidebar()

    # Render image upload section
    frontal_image_file, lateral_image_file = render_image_upload()

    # Render clinical information form
    clinical_form = render_clinical_form()

    # Process form submission
    if clinical_form["submit_button"]:
        if validate_inputs(frontal_image_file, lateral_image_file, clinical_form):
            # Load images
            frontal_image = Image.open(frontal_image_file)
            lateral_image = Image.open(lateral_image_file)

            # Generate report
            analysis = api_client.analyze_xray_images(
                frontal_image,
                lateral_image,
                clinical_form["indication"],
                clinical_form["comparison"] if clinical_form[
                    "comparison"] else "No prior studies available for comparison.",
                clinical_form["technique"],
                patient_info["patient_age"] if patient_info["patient_age"] else None,
                patient_info["patient_sex"] if patient_info["patient_sex"] != "Other" else None,
                patient_info["clinical_history"] if patient_info["clinical_history"] else None
            )

            # Display the report
            display_report(analysis, patient_info, clinical_form)


if __name__ == "__main__":
    main()