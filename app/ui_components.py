"""
UI components for the application.
"""

import streamlit as st
from datetime import datetime
from PIL import Image
from app.constants import DEFAULT_TECHNIQUE, ERROR_MISSING_IMAGES, ERROR_MISSING_INDICATION
from app.utils import (format_report_for_display, format_section_text, format_findings_text,
                       generate_report_text, generate_report_id, generate_doctor_signature)
from app.config_manager import config_manager


def render_sidebar():
    """Render the sidebar with patient information form."""
    with st.sidebar:
        st.header("Patient Information")
        st.markdown("---")

        patient_name = st.text_input("Patient Name", placeholder="Enter patient name")

        col1, col2 = st.columns(2)
        with col1:
            patient_age = st.number_input("Age", min_value=0, max_value=120, step=1)
        with col2:
            patient_sex = st.selectbox("Sex", options=["Male", "Female", "Other"])

        patient_id = st.text_input("Patient ID", placeholder="Enter patient ID")

        st.markdown("---")
        st.subheader("Additional Clinical Information")
        clinical_history = st.text_area("Clinical History",
                                        placeholder="Enter relevant patient history, symptoms, and risk factors")

    return {
        "patient_name": patient_name,
        "patient_age": patient_age,
        "patient_sex": patient_sex,
        "patient_id": patient_id,
        "clinical_history": clinical_history
    }


def render_image_upload():
    """Render the image upload section."""
    # Create two columns for image upload
    col1, col2 = st.columns(2)

    frontal_image_file = None
    lateral_image_file = None

    with col1:
        st.subheader("Frontal View (PA)")
        frontal_image_file = st.file_uploader("Upload frontal chest X-ray image",
                                              type=config_manager.settings.get("upload", {}).get("allowed_types",
                                                                                                 ["png", "jpg",
                                                                                                  "jpeg"]))
        if frontal_image_file is not None:
            frontal_image = Image.open(frontal_image_file)
            st.image(frontal_image, caption="Frontal (PA) View", use_column_width=True)

    with col2:
        st.subheader("Lateral View")
        lateral_image_file = st.file_uploader("Upload lateral chest X-ray image",
                                              type=config_manager.settings.get("upload", {}).get("allowed_types",
                                                                                                 ["png", "jpg",
                                                                                                  "jpeg"]))
        if lateral_image_file is not None:
            lateral_image = Image.open(lateral_image_file)
            st.image(lateral_image, caption="Lateral View", use_column_width=True)

    return frontal_image_file, lateral_image_file


def render_clinical_form():
    """Render the clinical information form."""
    st.markdown("---")
    st.subheader("Examination Details")

    with st.form("clinical_info"):
        col1, col2 = st.columns(2)

        with col1:
            indication = st.text_input("Clinical Indication",
                                       placeholder="E.g., Shortness of breath, chest pain, fever")
            technique = st.text_input("Technique",
                                      value=DEFAULT_TECHNIQUE,
                                      placeholder="E.g., PA and lateral views of the chest")

        with col2:
            comparison = st.text_input("Comparison Studies",
                                       placeholder="E.g., Previous study from 2023-10-15")
            exam_date = st.date_input("Examination Date", value=datetime.now())

        # Submit button
        st.markdown("---")
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            submit_button = st.form_submit_button("📋 GENERATE RADIOLOGY REPORT")

    return {
        "indication": indication,
        "technique": technique,
        "comparison": comparison,
        "exam_date": exam_date,
        "submit_button": submit_button
    }


def validate_inputs(frontal_image_file, lateral_image_file, clinical_form):
    """
    Validate user inputs before processing.

    Args:
        frontal_image_file: The frontal image file.
        lateral_image_file: The lateral image file.
        clinical_form: The clinical form data.

    Returns:
        bool: True if inputs are valid, False otherwise.
    """
    if frontal_image_file is None or lateral_image_file is None:
        st.error(ERROR_MISSING_IMAGES)
        return False

    if not clinical_form["indication"]:
        st.error(ERROR_MISSING_INDICATION)
        return False

    return True


def display_report(analysis, patient_info, clinical_form):
    """
    Display the radiology report.

    Args:
        analysis (str): The report analysis text.
        patient_info (dict): The patient information.
        clinical_form (dict): The clinical form data.
    """
    st.markdown("---")
    st.markdown("""
    <div class="report-section">
        <h2 class="report-header">Radiology Report</h2>
    """, unsafe_allow_html=True)

    # Add report header with patient info
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <table style="width: 100%; border: none;">
            <tr>
                <td><strong>Patient:</strong> {patient_info["patient_name"] if patient_info["patient_name"] else "Not specified"}</td>
                <td><strong>Patient ID:</strong> {patient_info["patient_id"] if patient_info["patient_id"] else "Not specified"}</td>
            </tr>
            <tr>
                <td><strong>Age:</strong> {patient_info["patient_age"] if patient_info["patient_age"] else "Not specified"}</td>
                <td><strong>Sex:</strong> {patient_info["patient_sex"] if patient_info["patient_sex"] != "Other" else "Not specified"}</td>
            </tr>
            <tr>
                <td><strong>Exam Date:</strong> {clinical_form["exam_date"].strftime('%Y-%m-%d')}</td>
                <td><strong>Report Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</td>
            </tr>
        </table>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    # Format and display the report sections
    section_content = format_report_for_display(analysis)

    # Display each section with proper formatting
    for section in config_manager.get_report_sections():
        section_key = f"{section}:"
        if section_key in section_content:
            st.markdown(f"<div class='report-subheader'>{section_key}</div>", unsafe_allow_html=True)

            # Handle the FINDINGS section specially (it often has sub-sections)
            if section_key == "FINDINGS:":
                findings_text = section_content[section_key]
                formatted_findings = format_findings_text(findings_text)
                st.markdown(f"<div class='findings'>{formatted_findings}</div>", unsafe_allow_html=True)
            else:
                # Process regular sections
                section_text = section_content[section_key]
                formatted_section = format_section_text(section_text)
                st.markdown(f"<div>{formatted_section}</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

    # Add disclaimer
    st.markdown(f"""
    <hr>
    <div class="disclaimer">
        {config_manager.get_disclaimer()}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Generate report for download
    report_txt = generate_report_text(
        analysis,
        patient_info["patient_name"],
        patient_info["patient_id"],
        patient_info["patient_age"],
        patient_info["patient_sex"],
        clinical_form["exam_date"]
    )

    # Add download buttons
    col1, col2 = st.columns(2)
    with col1:
        current_date = datetime.now().strftime("%Y-%m-%d")
        report_id = generate_report_id(patient_info["patient_name"])

        st.download_button(
            label="📄 Download Report (TXT)",
            data=report_txt,
            file_name=f"{report_id}_xray_report_{current_date}.txt",
            mime="text/plain"
        )

    # Add doctor signature
    with col2:
        st.markdown(generate_doctor_signature(), unsafe_allow_html=True)