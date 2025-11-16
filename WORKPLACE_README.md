# AWS Bedrock App Generator - Workplace Deployment Guide

**Status:** ✅ Production Ready  
**Last Updated:** November 15, 2025  
**For:** Teams and Enterprise Deployment

## 🎯 What This Project Does

Generates complete, production-ready applications (Python, Java, Node.js, etc.) using AWS Bedrock and Claude AI. Perfect for rapid prototyping and accelerating development at your workplace.

## 🚀 Fastest Way to Get Started (5 minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/TejaDev/aws-bedrock-app-generator.git
cd aws-bedrock-app-generator
```

### Step 2: Run Setup (One Command!)
```bash
# macOS/Linux
./setup.sh

# Windows
setup.bat
```

### Step 3: Configure AWS Credentials
```bash
# Option A: Using AWS CLI
aws configure

# Option B: Using environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### Step 4: Activate Environment & Generate Your First App
```bash
# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate.bat

# Generate Python REST API
python3 cli.py --name my_rest_api --requirements "REST API for user management" --type api --stack python

# Or generate Java microservice
python3 cli.py --name my_service --requirements "Spring Boot microservice" --type api --stack java
```

**Done!** Your app is in `generated_apps/my_rest_api` or `generated_apps/my_service`

## 📋 3 Deployment Methods for Your Team

### Method 1: Individual Laptops (Fastest Setup)
**Time:** 2-3 minutes | **For:** Single developers or quick testing

```bash
./setup.sh
source .venv/bin/activate
python3 cli.py --help
```

✅ Pros: Simple, fast, no dependencies  
❌ Cons: Each person sets up separately

**See:** `PORTABILITY_GUIDE.md` - Section "Local Virtual Environment"

### Method 2: Docker (Team Consistency)
**Time:** 5-10 minutes | **For:** Entire team, ensuring same environment

```bash
# Build once (team lead)
docker build -t bedrock-generator:latest .

# Each team member uses it
docker run -it \
  -v ~/.aws/credentials:/root/.aws/credentials:ro \
  -v $(pwd)/generated_apps:/app/generated_apps \
  bedrock-generator:latest
```

✅ Pros: Everyone has identical environment  
❌ Cons: Requires Docker

**See:** `PORTABILITY_GUIDE.md` - Section "Docker Container"

### Method 3: Makefile (Team Workflows)
**Time:** 30 seconds | **For:** Standardizing team commands

```bash
make help           # See all available commands
make setup          # Complete setup
make generate-py    # Generate Python app
make generate-java  # Generate Java app
make docker-build   # Build Docker image
```

✅ Pros: Simple, standardized commands  
❌ Cons: Requires Make (built-in on macOS/Linux)

**See:** `Makefile` in root directory

## 📚 Comprehensive Documentation

| Document | Purpose | Read When |
|----------|---------|-----------|
| `PORTABILITY_GUIDE.md` | Complete deployment guide | Planning deployment |
| `DEPLOYMENT_CHECKLIST.md` | Pre-deployment verification | Before going live |
| `README.md` | Project overview | First time reading |
| `QUICKSTART.py` | Code examples | Learning to use |
| `GENERATOR_ENHANCEMENTS.md` | Generator capabilities | Understanding features |
| `THROTTLING_GUIDE.md` | Performance tuning | Optimizing generation |

## 🔐 AWS Credentials at Your Workplace

### For Individual Development
```bash
aws configure
# Enter: AWS Access Key ID, Secret Access Key, Region (us-east-1)
```

### For Team Deployment (Recommended)
**Use IAM Role (no credentials in code):**
1. Request IAM role from your IT/Cloud team
2. Role needs `bedrock:InvokeModel` permission
3. Role automatically handles credentials

### For Docker Container
```bash
# Option A: Mount existing credentials
docker run -v ~/.aws/credentials:/root/.aws/credentials:ro bedrock-generator

# Option B: Pass via environment
docker run \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  bedrock-generator

# Option C: Use IAM role (EC2/ECS)
# Automatic - role attached to instance
```

## ⚙️ Essential Configuration

### Environment Variables (.env file)
```bash
# Copy .env.example to .env and fill in:
cp .env.example .env

# Edit .env with your settings:
AWS_REGION=us-east-1
OUTPUT_DIR=./generated_apps
LOG_LEVEL=INFO
```

### Project Structure
```
aws-bedrock-app-generator/
├── setup.sh                 # macOS/Linux setup
├── setup.bat               # Windows setup
├── Makefile                # Common commands
├── Dockerfile              # Container image
├── docker-compose.yml      # Container orchestration
├── .env.example            # Environment template
├── requirements.txt        # Dependencies
├── adaptive_app_gen/       # Main package
├── cli.py                  # Command-line interface
└── generated_apps/         # Output directory (created on first run)
```

## 🎓 Workplace Usage Examples

### Example 1: Developer Generates Python API
```bash
python3 cli.py \
  --name user-service \
  --requirements "REST API for user management with auth" \
  --type api \
  --stack python

# Generates complete project in generated_apps/user-service/
# Ready to: pip install -e . && python -m pytest
```

### Example 2: Team Builds Java Microservice
```bash
docker run -it \
  -v ~/.aws/credentials:/root/.aws/credentials:ro \
  -v $(pwd)/generated_apps:/app/generated_apps \
  bedrock-generator:latest \
  python cli.py \
    --name order-service \
    --requirements "Spring Boot microservice for order processing" \
    --type api \
    --stack java

# Generates in generated_apps/order-service/
# Ready to: mvn clean package && java -jar target/order-service.jar
```

### Example 3: Use Make for Consistency
```bash
# First time (one per team)
make docker-build

# Team members use same command
make generate-py
make generate-java
```

## 🔧 Troubleshooting at Workplace

### Python Not Installed
```bash
# macOS
brew install python@3.11

# Linux (Ubuntu)
sudo apt-get install python3.11

# Windows
# Download from https://www.python.org/downloads/
```

### AWS Credentials Not Working
```bash
# Test credentials
aws sts get-caller-identity

# If fails, request from your IT team that you have:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Appropriate permissions (bedrock:InvokeModel)
```

### Docker Permission Issues (Linux)
```bash
# Add user to docker group (one time)
sudo usermod -aG docker $USER
newgrp docker
```

### Bedrock Not Accessible
```bash
# Check region supports Bedrock
aws bedrock list-foundation-models --region us-east-1

# Valid regions: us-east-1, us-west-2, eu-central-1, ap-southeast-1
# Contact your AWS account team if access needed in different region
```

## 📊 Quick Reference

### Supported Tech Stacks
- ✅ Python (FastAPI, Flask, Django)
- ✅ Java (Spring Boot)
- ✅ Node.js (Express)
- ✅ TypeScript
- ✅ JavaScript

### Supported App Types
- ✅ Web (frontend frameworks)
- ✅ API (REST, microservices)
- ✅ CLI (command-line tools)
- ✅ Backend (services, workers)
- ✅ Desktop (Electron, PyQt)
- ✅ Mobile (React Native)

### Generation Time
- Average: 2-5 minutes per app
- First generation: May see throttling (automatic retry)
- Subsequent generations: Faster after AWS rate limits stabilize

## 🎯 Next Steps for Your Team

1. **Individual Setup** (5 min)
   ```bash
   ./setup.sh
   python3 cli.py --help
   ```

2. **Read Documentation** (10 min)
   - Check `PORTABILITY_GUIDE.md`
   - Check `QUICKSTART.py` for examples

3. **Generate Sample App** (3 min)
   ```bash
   python3 cli.py --name demo --requirements "Demo app" --stack python
   ```

4. **Review Generated Code** (5 min)
   - Look at `generated_apps/demo/`
   - Understand project structure
   - Check generated tests

5. **Deploy to Team Infrastructure** (varies)
   - Use Docker for consistency
   - Use Makefile for standardized commands
   - See `DEPLOYMENT_CHECKLIST.md`

## 📞 Support

### Common Questions

**Q: Can we use this in production?**  
A: Yes! Generated apps are production-ready with tests, configs, and best practices.

**Q: What about licensing?**  
A: Generated apps follow their tech stack licenses. See `LICENSE` file.

**Q: How much does it cost?**  
A: AWS Bedrock usage costs. Check AWS pricing. Generate once, use many times.

**Q: Can we customize the generated code?**  
A: Absolutely! Generated code is a starting point. Modify as needed.

**Q: What if Bedrock API fails?**  
A: Built-in retry logic with exponential backoff. See `THROTTLING_GUIDE.md`.

### Get Help

1. Check `TROUBLESHOOTING.md` in repository
2. Review `PORTABILITY_GUIDE.md` for your deployment method
3. Check GitHub issues: https://github.com/TejaDev/aws-bedrock-app-generator/issues
4. Contact: Your AWS account team for Bedrock-specific issues

## 📈 Scaling for Your Organization

### Small Team (1-5 developers)
- Use local virtual environment setup
- Share generated apps via Git
- Use AWS credentials configured locally

### Medium Team (5-20 developers)
- Use Docker for consistency
- Shared Docker registry (ECR, DockerHub)
- Central Git repository
- Use Makefile for standardized commands

### Large Organization (20+ developers)
- Deploy to Kubernetes or ECS
- Use AWS IAM roles (no credentials)
- Enterprise monitoring and logging
- See `PORTABILITY_GUIDE.md` - Section "Cloud Deployment"

## ✅ Verification Checklist

Before using at workplace:
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] AWS credentials configured (`aws sts get-caller-identity`)
- [ ] Can access AWS Bedrock (`aws bedrock list-foundation-models`)
- [ ] Git repository cloned (`git clone`)
- [ ] Setup script runs without errors (`./setup.sh`)
- [ ] Sample app generates successfully
- [ ] Generated app code looks reasonable
- [ ] Team has documented procedure
- [ ] Security review completed
- [ ] Costs estimated and approved

## 🎉 You're Ready!

Your workplace now has a powerful tool to generate complete applications instantly. Start with the quick start above, and refer to detailed documentation as needed.

**Happy building!** 🚀

---

**Project:** AWS Bedrock App Generator  
**Repository:** https://github.com/TejaDev/aws-bedrock-app-generator  
**Status:** ✅ Production Ready  
**Last Updated:** November 15, 2025
