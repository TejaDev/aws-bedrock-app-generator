"""Configuration management utilities"""

import os
from typing import Optional


class Config:
    """Application configuration"""
    
    # AWS Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
    AWS_BEDROCK_MODEL = os.getenv("AWS_BEDROCK_MODEL", "claude-3-5-sonnet-20241022")
    
    # Application Configuration
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./generated_apps")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Supported tech stacks
    SUPPORTED_TECH_STACKS = ["python", "nodejs", "typescript", "javascript", "java"]
    SUPPORTED_APP_TYPES = ["web", "cli", "api", "desktop", "mobile", "backend"]
    
    @staticmethod
    def validate_tech_stack(tech_stack: str) -> bool:
        """Validate if tech stack is supported"""
        return tech_stack.lower() in Config.SUPPORTED_TECH_STACKS
    
    @staticmethod
    def validate_app_type(app_type: str) -> bool:
        """Validate if app type is supported"""
        return app_type.lower() in Config.SUPPORTED_APP_TYPES
