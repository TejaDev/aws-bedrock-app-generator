#!/usr/bin/env python3
"""
Quick Start Guide - Adaptive Application Generator

This script walks through the setup and first run
"""

import subprocess
import sys
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n→ {description}")
    print(f"  Command: {cmd}\n")
    result = subprocess.run(cmd, shell=True, cwd="/Users/mst/Desktop/AWSBedRock")
    return result.returncode == 0

def main():
    print_header("Adaptive Application Generator - Quick Start")
    
    print("""
This guide will help you get started with the Adaptive Application Generator.

The tool generates complete, production-ready applications using AWS Bedrock
based on your specifications.
    """)
    
    # Step 1: Verify dependencies
    print_header("Step 1: Verify Dependencies")
    print("\nChecking if all dependencies are installed...")
    
    result = run_command(
        "python3 -c \"import boto3; import adaptive_app_gen.generators\"",
        "Verifying dependencies"
    )
    
    if not result:
        print("\n❌ Dependencies not installed. Run:")
        print("   pip3 install -r requirements.txt")
        return 1
    
    print("✓ All dependencies are installed")
    
    # Step 2: Check AWS configuration
    print_header("Step 2: Check AWS Configuration")
    print("\nVerifying AWS credentials...")
    
    result = run_command(
        "aws sts get-caller-identity",
        "Checking AWS credentials"
    )
    
    if not result:
        print("\n⚠️  AWS credentials not configured.")
        print("   Run: aws configure")
        print("   Or set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
        return 1
    
    print("✓ AWS credentials are configured")
    
    # Step 3: Show usage examples
    print_header("Step 3: Usage Examples")
    
    print("\n📝 Example 1: Generate a Python REST API")
    print("""
    python3 cli.py \\
      --name my_task_api \\
      --requirements "REST API for task management with CRUD operations" \\
      --type api \\
      --stack python
    """)
    
    print("\n📝 Example 2: Generate a Node.js CLI Tool")
    print("""
    python3 cli.py \\
      --name data_processor \\
      --requirements "CLI tool for processing and transforming CSV files" \\
      --type cli \\
      --stack nodejs
    """)
    
    print("\n📝 Example 3: Generate a TypeScript Web App")
    print("""
    python3 cli.py \\
      --name dashboard \\
      --requirements "Real-time dashboard with data visualization and authentication" \\
      --type web \\
      --stack typescript
    """)
    
    # Step 4: Run a test generation
    print_header("Step 4: Test Generation (Optional)")
    
    print("\n🧪 Run example demonstrations to see the generator in action:")
    print("   python3 example_usage.py")
    
    print("\n   This will generate 4 sample applications:")
    print("   1. Python REST API (task_api)")
    print("   2. Node.js CLI Tool (data_processor_cli)")
    print("   3. TypeScript Web App (dashboard_app)")
    print("   4. Python Backend Service (notification_service)")
    
    # Step 5: Next steps
    print_header("What's Next?")
    
    print("""
1. Generate Your First Application
   Run any of the examples above or customize with your own requirements

2. Explore Generated Projects
   Each generated app includes:
   - Full project structure
   - Main application code (AI-generated)
   - Configuration files
   - Test files
   - Dependencies list

3. Run the Generated Application
   cd generated_apps/<app_name>
   [Install dependencies]
   [Run according to app type]

4. Customize Generated Code
   All generated code is production-ready but can be customized
   Modify files in src/, config/, tests/ as needed
    """)
    
    # Step 6: Documentation
    print_header("Documentation")
    
    print("""
📚 Key Documentation Files:
- README.md: Complete feature and usage documentation
- IMPLEMENTATION_GUIDE.md: Technical architecture and design
- cli.py: Command-line interface with built-in help (--help flag)
- example_usage.py: Working examples for reference

📖 To see CLI help:
   python3 cli.py --help

🎓 For more information:
   - AWS Bedrock: https://docs.aws.amazon.com/bedrock/
   - Claude API: https://docs.anthropic.com/
    """)
    
    print_header("Ready to Generate!")
    
    print("""
You're all set! Your adaptive application generator is ready to use.

Quick command to get started:
    python3 cli.py --name myapp --requirements "Your app description" --type web --stack python

Happy generating! 🚀
    """)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
