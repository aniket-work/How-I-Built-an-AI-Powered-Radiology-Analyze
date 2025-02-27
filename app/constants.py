"""
Constants used throughout the application.
"""

import os
from pathlib import Path

# Project structure
ROOT_DIR = Path(__file__).parent.parent
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

# Configuration files
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.yaml")
PROMPTS_FILE = os.path.join(CONFIG_DIR, "prompts.json")

# Environment variables
ENV_VAR_API_KEY = "GROQ_API_KEY"

# Report sections
REPORT_SECTIONS = [
    "EXAMINATION:",
    "CLINICAL INFORMATION:",
    "COMPARISON:",
    "TECHNIQUE:",
    "FINDINGS:",
    "IMPRESSION:",
    "RECOMMENDATIONS:"
]

# Default values
DEFAULT_TECHNIQUE = "PA and lateral views of the chest"
DEFAULT_COMPARISON = "No prior studies available for comparison."

# Error messages
ERROR_API_KEY_MISSING = """
GROQ_API_KEY not found in environment. 
Please create a .env file with your Groq API key: GROQ_API_KEY=your_key_here
"""
ERROR_MISSING_IMAGES = "⚠️ Please upload both frontal and lateral X-ray images"
ERROR_MISSING_INDICATION = "⚠️ Please provide at least the clinical indication"

# Success messages
SUCCESS_GENERATING_REPORT = "Generating comprehensive radiology report..."

# File upload
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]