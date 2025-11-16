#!/usr/bin/env python3
"""
CLI interface for Adaptive Application Generator
Supports both interactive and command-line argument modes
"""

import argparse
import logging
import sys
from pathlib import Path

from adaptive_app_gen.generators import AdaptiveApplicationGenerator
from adaptive_app_gen.utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Adaptive Application Generator using AWS Bedrock",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode (recommended):
    python cli.py --interactive
  
  Generate a Python web application:
    python cli.py --name myapp --requirements "Create a REST API" --type web --stack python
  
  Generate a Node.js CLI tool:
    python cli.py --name mycli --requirements "Command-line tool for data processing" --type cli --stack nodejs
        """
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--name",
        help="Name of the application to generate"
    )
    
    parser.add_argument(
        "--requirements",
        help="Application requirements and description"
    )
    
    parser.add_argument(
        "--type",
        choices=Config.SUPPORTED_APP_TYPES,
        default="web",
        help="Type of application (default: web)"
    )
    
    parser.add_argument(
        "--stack",
        choices=Config.SUPPORTED_TECH_STACKS,
        default="python",
        help="Technology stack (default: python)"
    )
    
    parser.add_argument(
        "--output-dir",
        default=Config.OUTPUT_DIR,
        help=f"Output directory for generated apps (default: {Config.OUTPUT_DIR})"
    )
    
    parser.add_argument(
        "--no-tests",
        action="store_true",
        help="Skip generating test files"
    )
    
    parser.add_argument(
        "--region",
        default=Config.AWS_REGION,
        help=f"AWS region (default: {Config.AWS_REGION})"
    )
    
    args = parser.parse_args()
    
    # If interactive mode, import and run the interactive CLI
    if args.interactive or (not args.name and not args.requirements):
        try:
            from interactive_cli import InteractiveCLI
            cli = InteractiveCLI()
            return cli.run()
        except ImportError:
            logger.error("interactive_cli module not found")
            sys.exit(1)
    
    # Non-interactive mode
    try:
        # Validate inputs
        if not args.name:
            logger.error("Application name is required (--name)")
            sys.exit(1)
        
        if not args.requirements:
            logger.error("Application requirements are required (--requirements)")
            sys.exit(1)
        
        if not Config.validate_tech_stack(args.stack):
            logger.error(f"Unsupported tech stack: {args.stack}")
            sys.exit(1)
        
        if not Config.validate_app_type(args.type):
            logger.error(f"Unsupported app type: {args.type}")
            sys.exit(1)
        
        # Initialize generator
        logger.info("Initializing Adaptive Application Generator...")
        generator = AdaptiveApplicationGenerator(
            output_dir=args.output_dir,
            region=args.region
        )
        
        # Generate application
        logger.info(f"Generating application: {args.name}")
        result = generator.generate_application(
            requirements=args.requirements,
            app_name=args.name,
            app_type=args.type,
            tech_stack=args.stack,
            include_tests=not args.no_tests
        )
        
        # Display results
        print("\n" + "="*60)
        print("✓ Application Generated Successfully!")
        print("="*60)
        print(f"Application Name: {result['app_name']}")
        print(f"Project Path: {result['project_path']}")
        print(f"\nGenerated Files:")
        for file_name, file_path in result['generated_files'].items():
            print(f"  - {file_name}: {file_path}")
        print(f"\nConfiguration Files:")
        for file_name, file_path in result['config_files'].items():
            print(f"  - {file_name}: {file_path}")
        print(f"\nSpecification saved to: {result['project_path']}/APP_SPECIFICATION.json")
        print("="*60 + "\n")
        
        logger.info("Application generation completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Error generating application: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
