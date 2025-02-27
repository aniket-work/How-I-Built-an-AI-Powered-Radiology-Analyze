"""
Utility functions for the application.
"""

import streamlit as st
from datetime import datetime
from app.constants import REPORT_SECTIONS
from app.config_manager import config_manager


def format_report_for_display(analysis):
    """
    Format the report text for display in the UI.

    Args:
        analysis (str): The raw report text from the API.

    Returns:
        dict: A dictionary with each section's content.
    """
    # Get report sections from constants
    sections = REPORT_SECTIONS
    section_content = {}

    # Initialize with the full text
    remaining_text = analysis

    # Extract each section
    for i, section in enumerate(sections):
        if section in remaining_text:
            start_idx = remaining_text.find(section)

            # Find the start of the next section (if any)
            next_section_idx = float('inf')
            for next_section in sections[i + 1:]:
                if next_section in remaining_text[start_idx:]:
                    temp_idx = remaining_text[start_idx:].find(next_section)
                    if temp_idx < next_section_idx:
                        next_section_idx = temp_idx

            if next_section_idx != float('inf'):
                section_content[section] = remaining_text[
                                           start_idx + len(section):start_idx + next_section_idx].strip()
                remaining_text = remaining_text[start_idx + next_section_idx:]
            else:
                section_content[section] = remaining_text[start_idx + len(section):].strip()
                remaining_text = ""

    return section_content


def format_section_text(section_text):
    """
    Format the text for a regular section.

    Args:
        section_text (str): The section text.

    Returns:
        str: The formatted section text.
    """
    # Replace bullet points and emphasis
    formatted_text = section_text.replace(" * ", "<br>• ")
    formatted_text = formatted_text.replace("* ", "<br>• ")
    formatted_text = formatted_text.replace("**", "<strong>").replace("**", "</strong>")
    formatted_text = formatted_text.replace("*", "<em>").replace("*", "</em>")

    return formatted_text


def format_findings_text(findings_text):
    """
    Format the text for the FINDINGS section.

    Args:
        findings_text (str): The FINDINGS section text.

    Returns:
        str: The formatted FINDINGS section text.
    """
    # Replace bullet points formats
    formatted_text = findings_text.replace(" * ", "<br>• ")
    formatted_text = formatted_text.replace("* ", "<br>• ")

    # Handle sub-sections (typically labeled with letters a, b, c, etc.)
    for subsection in ["a.", "b.", "c.", "d.", "e.", "f.", "g.", "h."]:
        if subsection in formatted_text:
            formatted_text = formatted_text.replace(f"{subsection}",
                                                    f"<br><br><strong>{subsection}</strong>")

    # Remove asterisks used for emphasis
    formatted_text = formatted_text.replace("**", "<strong>").replace("**", "</strong>")
    formatted_text = formatted_text.replace("*", "<em>").replace("*", "</em>")

    return formatted_text


def generate_report_text(analysis, patient_name="", patient_id="",
                         patient_age="", patient_sex="", exam_date=None):
    """
    Generate the full report text for download.

    Args:
        analysis (str): The raw report text from the API.
        patient_name (str): The patient's name.
        patient_id (str): The patient's ID.
        patient_age (str): The patient's age.
        patient_sex (str): The patient's sex.
        exam_date (datetime): The examination date.

    Returns:
        str: The formatted report text.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    exam_date_str = exam_date.strftime('%Y-%m-%d') if exam_date else current_date
    disclaimer = config_manager.get_disclaimer()

    report_txt = f"""
CHEST X-RAY RADIOLOGY REPORT

Patient: {patient_name if patient_name else "Not specified"}
Patient ID: {patient_id if patient_id else "Not specified"}
Age: {patient_age if patient_age else "Not specified"}
Sex: {patient_sex if patient_sex != "Other" else "Not specified"}
Exam Date: {exam_date_str}
Report Date: {current_date}
----------------------------

{analysis}

----------------------------
DISCLAIMER: {disclaimer}
"""

    return report_txt


def generate_report_id(patient_name=""):
    """
    Generate a unique report ID.

    Args:
        patient_name (str): The patient's name.

    Returns:
        str: The report ID.
    """
    report_id = f"{patient_name.replace(' ', '_') if patient_name else 'Patient'}"
    return report_id


def generate_doctor_signature():
    """
    Generate a doctor signature HTML.

    Returns:
        str: The HTML for the doctor signature.
    """
    report_id = datetime.now().strftime("%Y%m%d%H%M%S")

    signature_html = f"""
    <div style="text-align: right; margin-top: 20px;">
        <p><em>Electronically signed by</em></p>
        <p style="font-weight: bold;">AI Assistant, MD</p>
        <p>Board Certified Radiologist</p>
        <p style="font-size: 0.8em;">Report ID: AI-XR-{report_id}</p>
    </div>
    """

    return signature_html