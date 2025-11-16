# Portability & Deployment Guide

This guide explains how to run the AWS Bedrock App Generator in different environments - from your laptop to enterprise deployments.

## 🚀 Quick Start (Any OS)

### Option 1: Automated Setup (Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```batch
setup.bat
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate it
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure AWS credentials
aws configure

# 5. Run the app
python3 cli.py --help
```

## 📦 Deployment Methods

### Method 1: Local Virtual Environment (Fastest)

**Setup Time:** 2-3 minutes  
**Requirements:** Python 3.9+, AWS credentials  
**Use When:** Single developer, testing locally

```bash
./setup.sh  # macOS/Linux
# or
setup.bat   # Windows

# Activate and use
source .venv/bin/activate
python3 cli.py --name my_app --requirements "..." --stack python
```

### Method 2: Docker Container (Most Portable)

**Setup Time:** 5-10 minutes  
**Requirements:** Docker, AWS credentials  
**Use When:** Team collaboration, CI/CD, consistent environments

#### Build Docker Image

```bash
docker build -t bedrock-generator:latest .
```

#### Run Container

```bash
# macOS/Linux - with AWS credentials
docker run -it \
  -v ~/.aws/credentials:/root/.aws/credentials:ro \
  -v $(pwd)/generated_apps:/app/generated_apps \
  -e AWS_REGION=us-east-1 \
  bedrock-generator:latest \
  python cli.py --name my_app --requirements "..." --stack python

# Windows PowerShell
docker run -it `
  -v $env:USERPROFILE\.aws\credentials:/root/.aws/credentials:ro `
  -v ${pwd}\generated_apps:/app/generated_apps `
  -e AWS_REGION=us-east-1 `
  bedrock-generator:latest `
  python cli.py --name my_app --requirements "..." --stack python
```

### Method 3: Docker Compose (Team Setup)

**Setup Time:** 3-5 minutes  
**Requirements:** Docker Compose  
**Use When:** Team environment, shared configurations

```bash
# Start the service
docker-compose up -d app-generator

# Run a generation
docker-compose exec app-generator python cli.py \
  --name my_app \
  --requirements "REST API" \
  --stack python

# View logs
docker-compose logs -f app-generator

# Stop the service
docker-compose down
```

### Method 4: Cloud Deployment (Production)

#### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04, t3.medium+)
# 2. SSH into instance
# 3. Clone repository
git clone https://github.com/TejaDev/aws-bedrock-app-generator.git
cd aws-bedrock-app-generator

# 4. Run setup
chmod +x setup.sh
./setup.sh

# 5. Configure AWS (IAM role or credentials)
aws configure

# 6. Use the generator
python3 cli.py --name my_app --requirements "..." --stack python
```

#### AWS Lambda (Serverless)

See `LAMBDA_DEPLOYMENT.md` for Lambda-specific setup.

#### ECS/Fargate (Container Orchestration)

```bash
# Build and push image
docker build -t 123456789.dkr.ecr.us-east-1.amazonaws.com/bedrock-gen:latest .
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/bedrock-gen:latest

# Deploy via CloudFormation/Terraform
# See CLOUD_DEPLOYMENT.md
```

## 🔐 AWS Credentials Setup

### Local Development

```bash
# Configure AWS CLI
aws configure

# Verify connection
aws bedrock list-foundation-models --region us-east-1
```

### Docker Container

```bash
# Option 1: Mount credentials file
docker run -v ~/.aws/credentials:/root/.aws/credentials:ro bedrock-generator

# Option 2: Use environment variables
docker run \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_REGION=us-east-1 \
  bedrock-generator

# Option 3: Use AWS_PROFILE
docker run \
  -e AWS_PROFILE=myprofile \
  -v ~/.aws/credentials:/root/.aws/credentials:ro \
  bedrock-generator
```

### Enterprise (SSO/IAM Roles)

```bash
# AWS SSO
aws sso login --profile production

# IAM Role (in EC2/Lambda/ECS)
# Automatic - attach role to instance
```

## 📋 System Requirements

### Minimum

- **OS:** macOS, Linux, Windows 10+
- **Python:** 3.9+ (3.11+ recommended)
- **RAM:** 2 GB
- **Disk:** 500 MB (+ space for generated apps)
- **Network:** Internet connection for AWS API calls

### Recommended for Teams

- **OS:** Any (Docker recommended)
- **Python:** 3.11+
- **RAM:** 4 GB
- **Disk:** 2+ GB
- **Docker:** 20.10+ (for containerized deployment)
- **AWS Account:** With Bedrock API access

## 🛠️ Troubleshooting

### Python not found

```bash
# Install Python 3.11
# macOS
brew install python@3.11

# Linux (Ubuntu)
sudo apt-get install python3.11 python3.11-venv

# Windows
# Download from https://www.python.org/downloads/
```

### AWS credentials error

```bash
# Verify credentials
aws sts get-caller-identity

# Check credential file
cat ~/.aws/credentials

# Set environment variables directly
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### Virtual environment not activating

```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate.bat  # Windows
```

### Docker permission denied

```bash
# macOS/Linux - add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Windows - run Docker Desktop as admin
```

### Bedrock API errors

```bash
# Verify Bedrock access
aws bedrock list-foundation-models --region us-east-1

# Check region (Bedrock available in limited regions)
# us-east-1, us-west-2, eu-central-1, ap-southeast-1

# Verify IAM permissions
# Need: bedrock:InvokeModel
```

## 📊 Environment Variables

### Core Configuration

```bash
# AWS
AWS_REGION=us-east-1                              # Bedrock region
AWS_BEDROCK_MODEL=us.anthropic.claude-3-5-sonnet-20241022-v2:0  # Model ID
AWS_PROFILE=default                               # AWS profile to use

# Application
OUTPUT_DIR=./generated_apps                       # Output directory
LOG_LEVEL=INFO                                    # DEBUG, INFO, WARNING, ERROR
DEBUG=False                                       # Enable debug mode

# Generation
MAX_TOKENS=2048                                   # Max tokens for generation
TEMPERATURE=0.7                                   # Generation temperature
```

### Development

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Use test mode (no actual generation)
export TEST_MODE=true

# Specify output directory
export OUTPUT_DIR=/path/to/output
```

## 🎯 Workflow Examples

### Single Developer

```bash
# 1. Setup once
./setup.sh

# 2. Generate apps as needed
source .venv/bin/activate
python3 cli.py --name app1 --requirements "..." --stack python
python3 cli.py --name app2 --requirements "..." --stack java
```

### Team Collaboration

```bash
# 1. Clone shared repo
git clone <repository>
cd aws-bedrock-app-generator

# 2. Each developer runs setup
./setup.sh
source .venv/bin/activate

# 3. Configure personal AWS credentials
aws configure

# 4. Generate and commit apps
python3 cli.py --name myfeature --requirements "..." --stack python
git add generated_apps/myfeature
git commit -m "Generated myfeature application"
git push
```

### Shared Infrastructure

```bash
# 1. Deploy Docker image to team server
docker build -t bedrock-gen:latest .
docker push myregistry.azurecr.io/bedrock-gen:latest

# 2. Team members use shared instance
docker run -v /shared/generated_apps:/app/generated_apps \
  myregistry.azurecr.io/bedrock-gen:latest \
  python cli.py --name app --requirements "..." --stack python
```

### CI/CD Pipeline

```yaml
# GitHub Actions example
name: Generate Application

on: [workflow_dispatch]

jobs:
  generate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t bedrock-gen .
      
      - name: Generate app
        run: |
          docker run \
            -e AWS_ACCESS_KEY_ID=${{ secrets.AWS_ACCESS_KEY_ID }} \
            -e AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }} \
            -v ${{ github.workspace }}/generated_apps:/app/generated_apps \
            bedrock-gen \
            python cli.py --name "${{ github.event.inputs.app_name }}" \
            --requirements "${{ github.event.inputs.requirements }}" \
            --stack "${{ github.event.inputs.stack }}"
      
      - name: Commit and push
        run: |
          git add generated_apps/
          git commit -m "Generated application"
          git push
```

## 📈 Performance Optimization

### For Large-Scale Generation

```bash
# Use cloud deployment
# See CLOUD_DEPLOYMENT.md for scaling options

# Docker resource limits
docker run \
  --memory=4g \
  --cpus=2 \
  bedrock-generator
```

### For Batch Operations

```bash
# Generate multiple apps efficiently
for app in app1 app2 app3; do
  python3 cli.py --name $app --requirements "..." --stack python
  sleep 30  # Avoid throttling
done
```

## 🔗 Related Documentation

- `README.md` - Project overview
- `QUICKSTART.py` - Quick examples
- `IMPLEMENTATION_GUIDE.md` - Architecture
- `GENERATOR_ENHANCEMENTS.md` - Template system
- `THROTTLING_GUIDE.md` - Performance tuning

## ✅ Verification Checklist

Before deploying to production:

- [ ] Python 3.9+ installed
- [ ] AWS credentials configured
- [ ] AWS Bedrock API accessible
- [ ] Generated apps working correctly
- [ ] Docker image built (if using containers)
- [ ] Environment variables documented
- [ ] Logs verified
- [ ] Error handling tested
- [ ] Security review completed (credentials, permissions)
- [ ] Performance tested

## 🆘 Support

For issues or questions:

1. Check `TROUBLESHOOTING.md`
2. Review `THROTTLING_GUIDE.md` for performance issues
3. Check GitHub issues: https://github.com/TejaDev/aws-bedrock-app-generator/issues
4. Review AWS Bedrock documentation: https://docs.aws.amazon.com/bedrock/

---

**Last Updated:** November 15, 2025  
**Status:** Production Ready ✓
