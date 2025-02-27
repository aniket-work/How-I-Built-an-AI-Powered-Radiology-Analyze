"""
API interaction module for making requests to the Groq API.
"""

import os
import requests
import streamlit as st
import json
from app.constants import ENV_VAR_API_KEY, SUCCESS_GENERATING_REPORT
from app.config_manager import config_manager
from app.prompt_builder import build_xray_analysis_prompt


class APIClient:
    """Client for interacting with the Groq API."""

    def __init__(self):
        """Initialize the API client."""
        self.api_key = os.getenv(ENV_VAR_API_KEY)
        self.endpoint = config_manager.get_api_endpoint()

    def is_configured(self):
        """Check if the API client is properly configured."""
        return bool(self.api_key and self.endpoint)

    def analyze_xray_images(self, frontal_image, lateral_image, indication, comparison, technique,
                            patient_age=None, patient_sex=None, clinical_history=None):
        """Use Groq API to generate a comprehensive radiology report."""
        try:
            # Build the prompt for the model
            prompt = build_xray_analysis_prompt(
                patient_age=patient_age,
                patient_sex=patient_sex,
                indication=indication,
                clinical_history=clinical_history,
                comparison=comparison,
                technique=technique
            )

            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # Get model parameters from configuration
            model_name = config_manager.get_model_name()
            model_params = config_manager.get_model_parameters()

            # Prepare the payload
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                **model_params
            }

            # Make the API request
            with st.spinner(SUCCESS_GENERATING_REPORT):
                response = requests.post(self.endpoint, headers=headers, json=payload)

            # Handle response
            if response.status_code != 200:
                st.error(f"Error from API: {response.text}")
                return f"Error: {response.status_code} - {response.text}"

            # Extract and return the analysis text
            analysis = response.json()["choices"][0]["message"]["content"]
            return analysis

        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}"


# Create a singleton instance
api_client = APIClient()