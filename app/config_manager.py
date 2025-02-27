"""
Configuration manager for the application.
Handles loading and accessing configuration from different sources.
"""

import os
import json
import yaml
from app.constants import CONFIG_FILE, SETTINGS_FILE, PROMPTS_FILE


class ConfigManager:
    """Manages application configuration from multiple sources."""

    def __init__(self):
        """Initialize the configuration manager."""
        self.config = {}
        self.settings = {}
        self.prompts = {}
        self._load_all()

    def _load_all(self):
        """Load all configuration files."""
        self._load_config()
        self._load_settings()
        self._load_prompts()

    def _load_config(self):
        """Load the main configuration from JSON."""
        try:
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config file: {e}")
            self.config = {}

    def _load_settings(self):
        """Load user-configurable settings from YAML."""
        try:
            with open(SETTINGS_FILE, 'r') as f:
                self.settings = yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error loading settings file: {e}")
            self.settings = {}

    def _load_prompts(self):
        """Load AI prompts from JSON."""
        try:
            with open(PROMPTS_FILE, 'r') as f:
                self.prompts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading prompts file: {e}")
            self.prompts = {}

    def get_api_config(self):
        """Get API configuration."""
        return self.config.get("api", {})

    def get_api_endpoint(self):
        """Get the API endpoint URL."""
        endpoints = self.get_api_config().get("endpoints", {})
        return endpoints.get("groq")

    def get_model_name(self):
        """Get the default model name."""
        # First check settings (user preference)
        settings_model = self.settings.get("api", {}).get("model")
        if settings_model:
            return settings_model

        # Fall back to config default
        return self.get_api_config().get("models", {}).get("default")

    def get_model_parameters(self):
        """Get model parameters (temperature, max_tokens, etc.)."""
        # Start with defaults from config
        params = self.get_api_config().get("parameters", {}).copy()

        # Override with settings if provided
        settings_temp = self.settings.get("api", {}).get("temperature")
        if settings_temp is not None:
            params["temperature"] = settings_temp

        settings_max_tokens = self.settings.get("api", {}).get("max_tokens")
        if settings_max_tokens is not None:
            params["max_tokens"] = settings_max_tokens

        return params

    def get_ui_config(self):
        """Get UI configuration."""
        return self.config.get("ui", {})

    def get_page_config(self):
        """Get Streamlit page configuration."""
        return {
            "page_title": self.settings.get("ui", {}).get("title"),
            "page_icon": self.settings.get("ui", {}).get("page_icon"),
            "layout": self.settings.get("ui", {}).get("layout"),
            "initial_sidebar_state": self.settings.get("ui", {}).get("initial_sidebar_state"),
        }

    def get_report_sections(self):
        """Get the report sections."""
        return self.settings.get("report", {}).get("sections", [])

    def get_findings_subsections(self):
        """Get the findings subsections."""
        return self.settings.get("report", {}).get("findings_subsections", [])

    def get_xray_prompt_template(self):
        """Get the X-ray analysis prompt template."""
        return self.prompts.get("xray_analysis", {})

    def get_disclaimer(self):
        """Get the report disclaimer text."""
        return self.config.get("report", {}).get("disclaimer", "")


# Create a singleton instance
config_manager = ConfigManager()