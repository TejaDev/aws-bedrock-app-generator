"""
AWS Bedrock client wrapper for adaptive application generation
"""

import json
import boto3
import time
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class BedrockClient:
    """Manages interactions with AWS Bedrock for content generation"""
    
    def __init__(self, region: str = "us-east-1", model_id: str = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"):
        """
        Initialize Bedrock client
        
        Args:
            region: AWS region
            model_id: Model ID to use (Claude 3.5 Sonnet via inference profile by default)
        """
        self.region = region
        self.model_id = model_id
        self.client = boto3.client("bedrock-runtime", region_name=region)
        logger.info(f"Initialized Bedrock client with model: {model_id}")
    
    def generate_content(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate content using Bedrock Converse API with retry logic
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation (0-1)
            
        Returns:
            Generated content as string
        """
        max_retries = 3
        retry_delay = 2  # seconds
        
        # Add small delay to avoid throttling
        time.sleep(0.5)
        
        for attempt in range(max_retries):
            try:
                response = self.client.converse(
                    modelId=self.model_id,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "text": prompt
                                }
                            ]
                        }
                    ],
                    inferenceConfig={
                        "maxTokens": max_tokens,
                        "temperature": temperature,
                    }
                )
                
                generated_text = response["output"]["message"]["content"][0]["text"]
                
                logger.info("Successfully generated content from Bedrock")
                return generated_text
                
            except Exception as e:
                if "ThrottlingException" in str(type(e)) or "Too many requests" in str(e):
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)  # exponential backoff
                        logger.warning(f"Throttled. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                
                logger.error(f"Error generating content: {str(e)}")
                raise
        
        raise Exception("Max retries exceeded")
    
    def generate_application_spec(
        self,
        requirements: str,
        app_type: str = "web",
        tech_stack: str = "python",
    ) -> Dict[str, Any]:
        """
        Generate application specifications based on requirements
        
        Args:
            requirements: User's application requirements
            app_type: Type of application (web, cli, api, etc.)
            tech_stack: Preferred tech stack
            
        Returns:
            Dictionary containing application specification
        """
        prompt = self._build_spec_prompt(requirements, app_type, tech_stack)
        response = self.generate_content(prompt, max_tokens=3000)
        
        try:
            # Try to parse as JSON
            spec = json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, create a structured spec
            spec = {
                "description": response,
                "app_type": app_type,
                "tech_stack": tech_stack,
                "requirements": requirements
            }
        
        return spec
    
    def generate_code(
        self,
        specification: Dict[str, Any],
        file_type: str = "main"
    ) -> str:
        """
        Generate code based on specification
        
        Args:
            specification: Application specification
            file_type: Type of file to generate (main, config, utils, etc.)
            
        Returns:
            Generated code as string
        """
        prompt = self._build_code_prompt(specification, file_type)
        code = self.generate_content(prompt, max_tokens=4000, temperature=0.2)
        return code
    
    def _build_spec_prompt(self, requirements: str, app_type: str, tech_stack: str) -> str:
        """Build prompt for generating application specification"""
        return f"""You are an expert software architect. Generate a detailed JSON specification for an application based on the following:

Application Type: {app_type}
Tech Stack: {tech_stack}
Requirements: {requirements}

Please provide a JSON specification with the following structure:
{{
    "name": "application name",
    "description": "brief description",
    "app_type": "{app_type}",
    "tech_stack": "{tech_stack}",
    "features": ["feature1", "feature2", ...],
    "project_structure": {{
        "directories": ["src", "tests", "config", ...],
        "main_files": ["main.py", "config.py", ...]
    }},
    "dependencies": ["dependency1", "dependency2", ...],
    "entry_point": "main file",
    "key_components": ["component1", "component2", ...]
}}

Generate only valid JSON, no additional text."""

    def _build_code_prompt(self, specification: Dict[str, Any], file_type: str) -> str:
        """Build prompt for generating code"""
        spec_str = json.dumps(specification, indent=2)
        
        return f"""You are an expert software developer. Generate production-quality {file_type} code for an application based on this specification:

{spec_str}

Requirements:
1. Generate clean, well-documented {file_type} code
2. Include proper error handling
3. Add type hints where applicable
4. Follow best practices for the tech stack
5. Include docstrings/comments for clarity
6. Generate only code, no markdown or explanations

Tech Stack: {specification.get('tech_stack', 'python')}
File Type: {file_type}

Generate the {file_type} code:"""
