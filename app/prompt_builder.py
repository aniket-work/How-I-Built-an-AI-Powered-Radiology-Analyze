"""
Module for building prompts to send to the AI model.
"""

from app.config_manager import config_manager


def _format_list_as_string(items):
    """Format a list as a string with each item on a new line with a dash."""
    return "\n".join([f"- {item}" for item in items])


def _format_subsection(subsection):
    """Format a findings subsection from the prompt template."""
    result = f"   {subsection['name']}:\n"
    for point in subsection.get('points', []):
        result += f"      - {point}\n"
    return result


def build_xray_analysis_prompt(patient_age=None, patient_sex=None,
                               indication="", clinical_history="",
                               comparison="", technique=""):
    """
    Build a prompt for X-ray image analysis.

    Args:
        patient_age: The patient's age (optional)
        patient_sex: The patient's sex (optional)
        indication: The clinical indication for the X-ray
        clinical_history: The patient's clinical history (optional)
        comparison: Previous studies for comparison (optional)
        technique: The imaging technique used

    Returns:
        str: The formatted prompt for the AI model
    """
    # Get prompt template from configuration
    template = config_manager.get_xray_prompt_template()

    # Start with the system role
    prompt = template.get("system_role", "")
    prompt += "\nYou are creating a comprehensive radiology report for chest X-ray images that have been uploaded for your interpretation.\n\n"

    # Add formatting instructions
    prompt += "IMPORTANT FORMATTING INSTRUCTIONS:\n"
    formatting_instructions = template.get("formatting_instructions", [])
    prompt += _format_list_as_string(formatting_instructions)
    prompt += "\n\n"

    # Add clinical context
    prompt += "CLINICAL CONTEXT:\n"
    prompt += f"- Patient Age: {patient_age if patient_age else 'Not provided'}\n"
    prompt += f"- Patient Sex: {patient_sex if patient_sex else 'Not provided'}\n"
    prompt += f"- Clinical Indication: {indication}\n"
    prompt += f"- Clinical History: {clinical_history if clinical_history else 'Not provided'}\n"
    prompt += f"- Comparison Studies: {comparison}\n"
    prompt += f"- Technique: {technique}\n\n"

    # Add X-ray image information
    prompt += "You have reviewed two high-quality chest X-ray images:\n"
    prompt += "1. A frontal (PA) view\n"
    prompt += "2. A lateral view\n\n"

    # Add report sections with descriptions
    prompt += "Based on your expertise and the clinical information provided, generate a comprehensive, professional-grade radiology report following the ACR (American College of Radiology) standard format:\n\n"

    for section in template.get("report_sections", []):
        section_name = section.get("name", "")
        section_desc = section.get("description", "")

        prompt += f"{section.get('index', '')}{section_name}: {section_desc}\n"

        # Add subsections for FINDINGS
        if section_name == "FINDINGS":
            prompt += "\n"
            for subsection in section.get("subsections", []):
                prompt += _format_subsection(subsection)

        # Add guidelines for certain sections
        if section.get("guidelines"):
            prompt += "   " + _format_list_as_string(section.get("guidelines", [])).replace("\n", "\n   ")

        prompt += "\n"

    # Add report quality guidelines
    prompt += "Your report should:\n"
    prompt += _format_list_as_string(template.get("report_quality_guidelines", []))

    # Add final instruction
    prompt += "\n\nWrite the report from the perspective of having thoroughly examined these specific X-ray images."

    return prompt