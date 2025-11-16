#!/usr/bin/env python3
"""
Interactive CLI for Adaptive Application Generator
Provides a user-friendly interface for generating applications interactively
"""

import logging
import sys
from pathlib import Path
from typing import List, Optional

from adaptive_app_gen.generators import AdaptiveApplicationGenerator
from adaptive_app_gen.utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class InteractiveCLI:
    """Interactive command-line interface for application generation"""
    
    def __init__(self):
        """Initialize the interactive CLI"""
        self.generator = None
        self.config = Config()
    
    @staticmethod
    def print_header(text: str) -> None:
        """Print a formatted header"""
        print("\n" + "="*70)
        print(f"  {text}")
        print("="*70)
    
    @staticmethod
    def print_section(text: str) -> None:
        """Print a formatted section"""
        print(f"\n→ {text}")
        print("-" * 70)
    
    @staticmethod
    def get_input(prompt: str, default: Optional[str] = None) -> str:
        """Get user input with optional default value"""
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        
        user_input = input(prompt).strip()
        return user_input if user_input else default or ""
    
    @staticmethod
    def get_choice(prompt: str, choices: List[str], default: int = 0) -> str:
        """Get user choice from a list"""
        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            marker = "→" if i - 1 == default else " "
            print(f"  {marker} {i}. {choice}")
        
        while True:
            try:
                choice_input = input(f"\nSelect option [1-{len(choices)}] (default: {default + 1}): ").strip()
                choice_num = int(choice_input) if choice_input else default + 1
                
                if 1 <= choice_num <= len(choices):
                    return choices[choice_num - 1]
                else:
                    print(f"Invalid choice. Please select between 1 and {len(choices)}")
            except ValueError:
                print("Please enter a valid number")
    
    @staticmethod
    def get_multiline_input(prompt: str, min_length: int = 10) -> str:
        """Get multiline input from user"""
        print(f"\n{prompt}")
        print("(Enter at least 3 lines, type 'END' on a new line when done)")
        print("-" * 70)
        
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        
        text = "\n".join(lines).strip()
        
        if len(text) < min_length:
            print(f"❌ Requirements too short (minimum {min_length} characters)")
            return InteractiveCLI.get_multiline_input(prompt, min_length)
        
        return text
    
    @staticmethod
    def get_yes_no(prompt: str, default: bool = True) -> bool:
        """Get yes/no input from user"""
        default_str = "Y/n" if default else "y/N"
        response = input(f"{prompt} [{default_str}]: ").strip().lower()
        
        if not response:
            return default
        
        return response in ["y", "yes"]
    
    def welcome(self) -> None:
        """Display welcome message"""
        self.print_header("Adaptive Application Generator - Interactive Mode")
        
        print("""
Welcome! This interactive tool will guide you through generating a 
production-ready application using AWS Bedrock and Claude AI.

Let's get started by collecting your application requirements.
        """)
    
    def get_app_name(self) -> str:
        """Get application name from user"""
        self.print_section("Step 1: Application Name")
        
        while True:
            app_name = self.get_input("Enter application name (e.g., 'task-api', 'data-processor')")
            
            if not app_name:
                print("❌ Application name cannot be empty")
                continue
            
            # Validate app name (alphanumeric and hyphens only)
            if not all(c.isalnum() or c == '-' for c in app_name):
                print("❌ Application name can only contain letters, numbers, and hyphens")
                continue
            
            if app_name.startswith('-') or app_name.endswith('-'):
                print("❌ Application name cannot start or end with a hyphen")
                continue
            
            print(f"✓ Application name: {app_name}")
            return app_name
    
    def get_app_type(self) -> str:
        """Get application type from user"""
        self.print_section("Step 2: Application Type")
        
        app_types = self.config.SUPPORTED_APP_TYPES
        print("What type of application would you like to create?")
        
        selected_type = self.get_choice(
            "Select application type:",
            app_types,
            default=app_types.index("web") if "web" in app_types else 0
        )
        
        print(f"✓ Application type: {selected_type}")
        return selected_type
    
    def get_tech_stack(self) -> str:
        """Get technology stack from user"""
        self.print_section("Step 3: Technology Stack")
        
        stacks = self.config.SUPPORTED_TECH_STACKS
        print("Which technology stack do you prefer?")
        
        selected_stack = self.get_choice(
            "Select technology stack:",
            stacks,
            default=stacks.index("python") if "python" in stacks else 0
        )
        
        print(f"✓ Technology stack: {selected_stack}")
        return selected_stack
    
    def get_requirements(self) -> str:
        """Get application requirements from user"""
        self.print_section("Step 4: Application Requirements")
        
        print("""
Please describe your application requirements in detail.
Include information about:
- Main features and functionality
- User interactions
- Data models and storage
- Integration points
- Performance requirements
- Any specific technologies or frameworks
        """)
        
        requirements = self.get_multiline_input(
            "Enter your application requirements:"
        )
        
        print(f"\n✓ Requirements collected ({len(requirements)} characters)")
        return requirements
    
    def get_aws_settings(self) -> tuple:
        """Get AWS configuration settings"""
        self.print_section("Step 5: AWS Configuration (Optional)")
        
        output_dir = self.get_input(
            "Output directory for generated applications",
            default=self.config.OUTPUT_DIR
        )
        
        region = self.get_input(
            "AWS region",
            default=self.config.AWS_REGION
        )
        
        print(f"✓ Output directory: {output_dir}")
        print(f"✓ AWS region: {region}")
        
        return output_dir, region
    
    def get_additional_options(self) -> dict:
        """Get additional generation options"""
        self.print_section("Step 6: Additional Options")
        
        include_tests = self.get_yes_no(
            "Include test files in generated application?",
            default=True
        )
        
        options = {
            "include_tests": include_tests,
        }
        
        print(f"✓ Include tests: {include_tests}")
        
        return options
    
    def confirm_generation(self, app_config: dict) -> bool:
        """Display summary and confirm generation"""
        self.print_section("Confirm Application Generation")
        
        print("""
Here's a summary of your application configuration:
        """)
        
        print(f"  Application Name:    {app_config['app_name']}")
        print(f"  Type:                {app_config['app_type']}")
        print(f"  Technology Stack:    {app_config['tech_stack']}")
        print(f"  Output Directory:    {app_config['output_dir']}")
        print(f"  AWS Region:          {app_config['region']}")
        print(f"  Include Tests:       {app_config['include_tests']}")
        
        print(f"\n  Requirements ({len(app_config['requirements'])} characters):")
        # Print first 200 characters of requirements
        preview = app_config['requirements'][:200]
        if len(app_config['requirements']) > 200:
            preview += "..."
        print(f"  {preview}")
        
        confirm = self.get_yes_no("\nProceed with generation?", default=True)
        
        return confirm
    
    def generate_application(self, app_config: dict) -> Optional[dict]:
        """Generate the application"""
        self.print_header("Generating Your Application...")
        
        try:
            # Initialize generator
            self.generator = AdaptiveApplicationGenerator(
                output_dir=app_config['output_dir'],
                region=app_config['region']
            )
            
            # Generate application
            print(f"\n⏳ Generating {app_config['app_name']}...\n")
            
            result = self.generator.generate_application(
                requirements=app_config['requirements'],
                app_name=app_config['app_name'],
                app_type=app_config['app_type'],
                tech_stack=app_config['tech_stack'],
                include_tests=app_config['include_tests']
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating application: {str(e)}", exc_info=True)
            print(f"\n❌ Error: {str(e)}")
            return None
    
    def display_results(self, result: dict) -> None:
        """Display generation results"""
        self.print_header("✓ Application Generated Successfully!")
        
        print(f"""
Application Name:  {result.get('app_name', 'N/A')}
Project Path:      {result.get('project_path', 'N/A')}

Generated Files ({len(result.get('generated_files', {}))}):
        """)
        
        for file_name, file_path in result.get('generated_files', {}).items():
            print(f"  • {file_name}")
            print(f"    └─ {file_path}")
        
        print(f"\nConfiguration Files ({len(result.get('config_files', {}))}):")
        
        for file_name, file_path in result.get('config_files', {}).items():
            print(f"  • {file_name}")
            print(f"    └─ {file_path}")
        
        spec_path = Path(result.get('project_path', '')) / 'APP_SPECIFICATION.json'
        print(f"\nSpecification:     {spec_path}")
        
        print(f"""
Next Steps:
  1. Navigate to the project directory:
     cd {result.get('project_path', 'generated_app')}
  
  2. Review the README.md for setup instructions
  
  3. Install dependencies and run the application according to its type
  
  4. Customize the generated code as needed

Happy coding! 🚀
        """)
    
    def run(self) -> int:
        """Run the interactive CLI"""
        try:
            self.welcome()
            
            # Collect all inputs
            app_name = self.get_app_name()
            app_type = self.get_app_type()
            tech_stack = self.get_tech_stack()
            requirements = self.get_requirements()
            output_dir, region = self.get_aws_settings()
            additional_options = self.get_additional_options()
            
            # Prepare configuration
            app_config = {
                "app_name": app_name,
                "app_type": app_type,
                "tech_stack": tech_stack,
                "requirements": requirements,
                "output_dir": output_dir,
                "region": region,
                **additional_options
            }
            
            # Confirm before generation
            if not self.confirm_generation(app_config):
                print("\n❌ Generation cancelled by user")
                return 1
            
            # Generate application
            result = self.generate_application(app_config)
            
            if not result:
                return 1
            
            # Display results
            self.display_results(result)
            
            logger.info("Application generation completed successfully!")
            return 0
            
        except KeyboardInterrupt:
            print("\n\n❌ Generation cancelled by user (Ctrl+C)")
            return 1
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            print(f"\n❌ Unexpected error: {str(e)}")
            return 1


def main():
    """Main entry point"""
    cli = InteractiveCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
