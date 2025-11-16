#!/usr/bin/env python3
"""
Example usage of Adaptive Application Generator
Demonstrates how to use the generator programmatically
"""

import logging
from adaptive_app_gen.generators import AdaptiveApplicationGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_1_python_api():
    """Example 1: Generate a Python REST API application"""
    print("\n" + "="*60)
    print("Example 1: Generating Python REST API")
    print("="*60 + "\n")
    
    generator = AdaptiveApplicationGenerator(output_dir="./generated_apps")
    
    result = generator.generate_application(
        app_name="task_api",
        requirements="""
        Create a REST API for task management with the following features:
        - Create, read, update, delete tasks
        - Task categories and priorities
        - User authentication
        - Task filtering and sorting
        - Pagination support
        """,
        app_type="api",
        tech_stack="python",
        include_tests=True
    )
    
    print("\nGeneration Result:")
    print(f"✓ Project created at: {result['project_path']}")
    print(f"✓ Generated files: {len(result['generated_files'])}")
    print(f"✓ Config files: {len(result['config_files'])}")
    

def example_2_nodejs_cli():
    """Example 2: Generate a Node.js CLI tool"""
    print("\n" + "="*60)
    print("Example 2: Generating Node.js CLI Tool")
    print("="*60 + "\n")
    
    generator = AdaptiveApplicationGenerator(output_dir="./generated_apps")
    
    result = generator.generate_application(
        app_name="data_processor_cli",
        requirements="""
        Create a command-line tool for data processing with:
        - CSV file parsing and transformation
        - Data validation and filtering
        - Export to multiple formats (JSON, XML, SQL)
        - Progress reporting
        - Error logging and recovery
        """,
        app_type="cli",
        tech_stack="nodejs",
        include_tests=True
    )
    
    print("\nGeneration Result:")
    print(f"✓ Project created at: {result['project_path']}")
    print(f"✓ Generated files: {len(result['generated_files'])}")
    print(f"✓ Config files: {len(result['config_files'])}")


def example_3_typescript_web():
    """Example 3: Generate a TypeScript web application"""
    print("\n" + "="*60)
    print("Example 3: Generating TypeScript Web Application")
    print("="*60 + "\n")
    
    generator = AdaptiveApplicationGenerator(output_dir="./generated_apps")
    
    result = generator.generate_application(
        app_name="dashboard_app",
        requirements="""
        Create a real-time dashboard application with:
        - Live data visualization with charts and graphs
        - User authentication and authorization
        - Dark/light theme support
        - Responsive design for mobile and desktop
        - Real-time notifications
        - Data export functionality
        """,
        app_type="web",
        tech_stack="typescript",
        include_tests=True
    )
    
    print("\nGeneration Result:")
    print(f"✓ Project created at: {result['project_path']}")
    print(f"✓ Generated files: {len(result['generated_files'])}")
    print(f"✓ Config files: {len(result['config_files'])}")


def example_4_python_backend():
    """Example 4: Generate a Python backend service"""
    print("\n" + "="*60)
    print("Example 4: Generating Python Backend Service")
    print("="*60 + "\n")
    
    generator = AdaptiveApplicationGenerator(output_dir="./generated_apps")
    
    result = generator.generate_application(
        app_name="notification_service",
        requirements="""
        Create a notification service backend with:
        - Email and SMS notification support
        - Message queuing and scheduling
        - Template management
        - Delivery tracking and retry logic
        - Rate limiting and throttling
        - Analytics and reporting
        """,
        app_type="backend",
        tech_stack="python",
        include_tests=True
    )
    
    print("\nGeneration Result:")
    print(f"✓ Project created at: {result['project_path']}")
    print(f"✓ Generated files: {len(result['generated_files'])}")
    print(f"✓ Config files: {len(result['config_files'])}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Adaptive Application Generator - Examples")
    print("="*60)
    print("\nRunning examples to demonstrate application generation...")
    
    try:
        # Run examples
        example_1_python_api()
        example_2_nodejs_cli()
        example_3_typescript_web()
        example_4_python_backend()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("Check the './generated_apps' directory for generated projects")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Error running examples: {str(e)}", exc_info=True)
