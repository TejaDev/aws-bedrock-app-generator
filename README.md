# Adaptive Application Generator

Generate production-ready applications using AWS Bedrock and Claude AI.

## Quick Start

```bash
# Interactive mode (recommended)
python3 generate.py

# Or use CLI directly
python3 cli.py --name myapp --requirements "REST API for task management" --type api --stack python
```

## Installation

```bash
pip3 install -r requirements.txt
aws configure  # Configure AWS credentials
```

## Features

- ✅ Intelligent code generation with Claude 3.5 Sonnet
- ✅ Multi-stack support: Python, Node.js, TypeScript, Java
- ✅ Multiple app types: Web, API, CLI, Backend
- ✅ Auto-generated tests and configuration
- ✅ Complete project structures
- ✅ AWS Bedrock integration

## Supported Tech

| Type | Options |
|------|---------|
| **Languages** | Python, Node.js, TypeScript, JavaScript |
| **App Types** | web, api, cli, backend, desktop, mobile |

## CLI Usage

```bash
python3 cli.py \
  --name my_app \
  --requirements "Application description" \
  --type api \
  --stack python
```

### Options
- `--name` - Application name (required in CLI mode)
- `--requirements` - App description (required in CLI mode)
- `--type` - App type: web, api, cli, backend, desktop, mobile (default: web)
- `--stack` - Tech stack: python, nodejs, typescript, javascript (default: python)
- `--output-dir` - Output directory (default: ./generated_apps)
- `--no-tests` - Skip test generation
- `--region` - AWS region (default: us-east-1)

## After Generation

```bash
cd generated_apps/your-app
./setup.sh          # Install dependencies
python -m your_app  # Run the app
```

## Documentation

- **GET_STARTED.md** - Quick start and setup
- **QUICK_REFERENCE.md** - Commands and examples
- **IMPLEMENTATION_GUIDE.md** - Technical architecture
- **GENERATOR_ENHANCEMENTS.md** - Enhancement details
- **README.md Appendices** - Deployment, throttling, and environments

## Prerequisites

- Python 3.9+
- AWS Account with Bedrock access
- AWS credentials configured

## Architecture

```
adaptive_app_gen/
├── bedrock_client.py       # AWS Bedrock integration
├── generators/
│   ├── app_generator.py    # Main orchestrator
│   ├── python_generator.py # Python-specific generation
│   └── java_generator.py   # Java-specific generation
└── utils/
    └── config.py           # Configuration
```

## Generated Project Structure

```
your_app/
├── src/
│   ├── api/               # API routes
│   ├── middleware/        # Custom middleware
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   └── utils/            # Utilities (logger, validators, helpers)
├── config/               # Configuration files
├── tests/                # Test files
├── requirements.txt      # Python dependencies
└── APP_SPECIFICATION.json # Generated specification
```

## Examples

### Python REST API
```bash
python3 generate.py
# Select: api → python → describe requirements
```

### Node.js CLI Tool
```bash
python3 cli.py \
  --name csv_processor \
  --requirements "CLI tool for CSV processing and conversion" \
  --type cli \
  --stack nodejs
```

### TypeScript Web App
```bash
python3 cli.py \
  --name dashboard \
  --requirements "Real-time dashboard with authentication" \
  --type web \
  --stack typescript
```

## Troubleshooting

**AWS Bedrock Access Error**
- Run `aws configure` to set up credentials
- Verify IAM permissions for bedrock-runtime
- Check that Bedrock is available in your region

**Import Errors in Generated App**
- Run `./setup.sh` in the generated app directory
- Verify Python 3.9+ is being used
- Check that all dependencies installed correctly

**Generation Fails**
- Ensure requirements are descriptive
- Check AWS Bedrock quota limits
- Verify AWS credentials are valid

## Use Cases

- 🚀 Rapid prototyping and MVP development
- 📚 Learning AI-generated code patterns
- 📋 Bootstrap new projects with full structure
- 🔍 Technology exploration and comparison
- 👥 Team onboarding with consistent templates
- ✨ Proof of concepts for presentations

## License

MIT

---

**Built with AWS Bedrock and Claude AI**

---

## Appendix: Deployment & Portability

### Local Setup

**macOS/Linux:**
```bash
chmod +x setup.sh && ./setup.sh
```

**Windows:**
```bash
setup.bat
```

### Docker Deployment

```bash
# Build image
docker build -t bedrock-generator:latest .

# Run with credentials
docker run -it \
  -v ~/.aws/credentials:/root/.aws/credentials:ro \
  -v $(pwd)/generated_apps:/app/generated_apps \
  -e AWS_REGION=us-east-1 \
  bedrock-generator:latest \
  python cli.py --name myapp --requirements "..." --stack python
```

### Docker Compose

```bash
docker-compose up -d app-generator
docker-compose exec app-generator python cli.py --name myapp --requirements "..." --stack python
```

### AWS Deployment

**EC2:**
```bash
git clone <repo>
cd aws-bedrock-app-generator
./setup.sh
aws configure
python3 cli.py --name myapp --requirements "..." --stack python
```

### AWS Credentials

```bash
# Configure locally
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1

# Verify connection
aws bedrock list-foundation-models --region us-east-1
```

### System Requirements

| Minimum | Recommended |
|---------|-------------|
| Python 3.9+ | Python 3.11+ |
| 2 GB RAM | 4 GB RAM |
| 500 MB disk | 2+ GB disk |
| macOS/Linux/Windows | Any (Docker for teams) |

### Troubleshooting Deployment

**AWS credentials error:**
```bash
aws sts get-caller-identity  # Verify credentials
cat ~/.aws/credentials        # Check credential file
```

**Virtual environment issues:**
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Docker permission denied:**
```bash
sudo usermod -aG docker $USER  # macOS/Linux
# Windows: Run Docker Desktop as admin
```

---

## Appendix: Throttling & Performance

### Understanding Throttling

AWS Bedrock has rate limits on API calls. When you exceed them, requests are temporarily throttled. This is **normal and expected** behavior.

**Automatic handling:**
- ✅ Retries enabled (up to 3 attempts)
- ✅ Exponential backoff (2s, 4s, 8s delays)
- ✅ Transparent to users (logged as warnings)

### Best Practices

1. **Generate apps sequentially** - one at a time
2. **Wait for completion** - before starting next
3. **Add delays** - 30-60 seconds between generations
4. **Monitor logs** - "Throttled" warnings are normal

### Example Batch Generation

```bash
# Generate multiple apps with delays
python3 cli.py --name app1 --requirements "..." --stack java
sleep 30
python3 cli.py --name app2 --requirements "..." --stack java
sleep 30
python3 cli.py --name app3 --requirements "..." --stack java
```

### Typical Generation Times

- Simple API: 2-3 minutes
- Complex backend: 3-5 minutes
- With throttling: Add 10-20 seconds

### If Throttling Persists

1. **Use a different model** - Switch to Claude Haiku (faster, higher limits)
   ```bash
   export AWS_BEDROCK_MODEL=us.anthropic.claude-3-5-haiku-20241022-v1:0
   ```

2. **Request higher limits** - Contact AWS Support via AWS Console → Bedrock → Usage Quotas

3. **Increase inter-call delays** - Modify `bedrock_client.py` to add longer delays

### Monitoring

Check logs for throttling messages (normal behavior):
```
WARNING - Throttled. Retrying in 2s... (attempt 1/3)
WARNING - Throttled. Retrying in 4s... (attempt 2/3)
INFO - Successfully generated content from Bedrock
```

---

## Environment Variables

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default
AWS_BEDROCK_MODEL=us.anthropic.claude-3-5-sonnet-20241022-v2:0

# Application
OUTPUT_DIR=./generated_apps
LOG_LEVEL=INFO
DEBUG=false

# Generation
MAX_TOKENS=2048
TEMPERATURE=0.7
```

---

**Last Updated:** November 15, 2025
