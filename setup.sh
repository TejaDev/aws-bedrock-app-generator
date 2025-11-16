#!/bin/bash
# AWS Bedrock App Generator - Setup Script
# This script sets up the project for any environment

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   AWS Bedrock App Generator - Setup                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Step 1: Check Python version
echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.9 or higher from https://www.python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
print_status "Python $PYTHON_VERSION found"

# Step 2: Check AWS credentials
echo ""
echo "Step 2: Checking AWS credentials..."
if [ -z "$AWS_ACCESS_KEY_ID" ] && [ ! -f ~/.aws/credentials ]; then
    print_error "AWS credentials not configured"
    echo "Please set up AWS credentials using one of the following methods:"
    echo "  1. Run: aws configure"
    echo "  2. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables"
    echo "  3. Create ~/.aws/credentials file"
    exit 1
fi
print_status "AWS credentials found"

# Step 3: Create virtual environment
echo ""
echo "Step 3: Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    print_status "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate
print_status "Virtual environment activated"

# Step 4: Install dependencies
echo ""
echo "Step 4: Installing dependencies..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -q -r requirements.txt
print_status "Dependencies installed"

# Step 5: Verify installation
echo ""
echo "Step 5: Verifying installation..."
python3 -c "import boto3; print(f'  boto3: {boto3.__version__}')" 2>/dev/null && print_status "boto3 installed" || print_error "boto3 not found"
python3 -c "import adaptive_app_gen; print('  adaptive_app_gen: OK')" 2>/dev/null && print_status "adaptive_app_gen module OK" || print_error "adaptive_app_gen not found"

# Step 6: Check AWS Bedrock access
echo ""
echo "Step 6: Checking AWS Bedrock access..."
if python3 -c "from adaptive_app_gen.bedrock_client import BedrockClient; client = BedrockClient(); print('  Connection OK')" 2>/dev/null; then
    print_status "AWS Bedrock access verified"
else
    print_info "AWS Bedrock access check skipped (will test on first generation)"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Setup Complete!                                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Activate environment: source .venv/bin/activate"
echo "  2. Generate an app:     python3 cli.py --help"
echo "  3. Read docs:           cat QUICKSTART.md"
echo ""
