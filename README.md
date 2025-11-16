# Adaptive Application Generator using AWS Bedrock

A powerful tool that demonstrates **Adaptive Application Generation** - automatically generating complete application projects based on user requirements using AWS Bedrock and Claude AI models.

## 🎯 Features

- **Intelligent Application Generation**: Create full application structures with code and configuration
- **Multi-Tech Stack Support**: Generate applications in Python, Node.js, TypeScript, and JavaScript
- **Adaptive Architecture**: Automatically adapts generated code to different application types (web, API, CLI, backend, etc.)
- **Complete Project Structure**: Generates organized directory layouts, configuration files, and dependencies
- **Test Generation**: Automatically creates test files for your generated applications
- **AWS Bedrock Integration**: Uses Claude 3.5 Sonnet for high-quality code generation
- **CLI and Programmatic Interfaces**: Use via command-line or import as a Python module

## 🏗️ Project Structure

```
adaptive_app_gen/
├── __init__.py                 # Package initialization
├── bedrock_client.py          # AWS Bedrock client wrapper
├── generators/
│   ├── __init__.py
│   └── app_generator.py       # Main application generator
└── utils/
    ├── __init__.py
    ├── config.py              # Configuration management
    └── templates/             # Template files (for future expansion)

cli.py                          # Command-line interface
example_usage.py               # Example demonstrations
requirements.txt               # Python dependencies
```

## 📦 Installation

### Prerequisites
- Python 3.9+
- AWS Account with Bedrock access
- AWS credentials configured (via AWS CLI or environment variables)

### Setup

1. **Clone or download the project** to your machine

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure AWS Credentials**:
   ```bash
   aws configure
   ```
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   export AWS_REGION=us-east-1
   ```

## 🚀 Quick Start

### Using the CLI

Generate a Python REST API:
```bash
python3 cli.py \
  --name my_task_api \
  --requirements "Create a REST API for task management with CRUD operations" \
  --type api \
  --stack python
```

Generate a Node.js CLI tool:
```bash
python3 cli.py \
  --name data_processor \
  --requirements "Create a CLI tool for processing CSV files" \
  --type cli \
  --stack nodejs
```

### Using the Python API

```python
from adaptive_app_gen.generators import AdaptiveApplicationGenerator

# Initialize generator
generator = AdaptiveApplicationGenerator(output_dir="./my_apps")

# Generate an application
result = generator.generate_application(
    app_name="my_app",
    requirements="Create a REST API with authentication",
    app_type="api",
    tech_stack="python",
    include_tests=True
)

print(f"App generated at: {result['project_path']}")
```

## 📋 Supported Tech Stacks

- **Python**: FastAPI, Django, Flask, etc.
- **Node.js**: Express, NestJS, etc.
- **TypeScript**: Full TypeScript support for modern applications
- **JavaScript**: Modern ES6+ JavaScript

## 🎨 Supported Application Types

- **web**: Web applications and frontends
- **api**: REST APIs and services
- **cli**: Command-line tools and utilities
- **backend**: Backend services and microservices
- **desktop**: Desktop applications
- **mobile**: Mobile applications (React Native, Flutter)

## 🔧 CLI Options

```
usage: cli.py [-h] --name NAME --requirements REQUIREMENTS 
              [--type {web,cli,api,desktop,mobile,backend}]
              [--stack {python,nodejs,typescript,javascript}]
              [--output-dir OUTPUT_DIR] [--no-tests] [--region REGION]

options:
  --name NAME              Name of the application
  --requirements REQUIREMENTS
                          Application requirements and description
  --type {web,...}        Application type (default: web)
  --stack {python,...}    Technology stack (default: python)
  --output-dir DIR        Output directory (default: ./generated_apps)
  --no-tests             Skip generating test files
  --region REGION        AWS region (default: us-east-1)
```

## 📝 Examples

### Example 1: Python API
```bash
python3 cli.py \
  --name task_manager_api \
  --requirements "REST API with user authentication, task CRUD, categories, and filtering" \
  --type api \
  --stack python
```

### Example 2: Node.js CLI
```bash
python3 cli.py \
  --name csv_processor \
  --requirements "CLI tool for CSV transformation, validation, and export to JSON/XML" \
  --type cli \
  --stack nodejs
```

### Example 3: TypeScript Web App
```bash
python3 cli.py \
  --name dashboard \
  --requirements "Real-time dashboard with charts, authentication, and theme support" \
  --type web \
  --stack typescript
```

### Run Multiple Examples
```bash
python3 example_usage.py
```

## 🏃 Running Generated Applications

Each generated application includes:
1. **Main entry point** (main.py, main.js, etc.)
2. **Configuration files** (config.py, package.json, etc.)
3. **Dependencies** (requirements.txt, package.json)
4. **Test files** (tests/ directory with sample tests)
5. **Project structure** organized by feature/component

To run a generated application:

**Python**:
```bash
cd generated_apps/my_app
pip install -r requirements.txt
python src/main.py
```

**Node.js/TypeScript**:
```bash
cd generated_apps/my_app
npm install
npm start
```

## 🔐 AWS Bedrock Configuration

### Available Models
- **Claude 3.5 Sonnet** (default): Best quality, suitable for complex applications
- **Claude 3.5 Haiku**: Cost-effective, suitable for simpler applications

### Setting Model
```bash
export AWS_BEDROCK_MODEL=claude-3-5-haiku-20241022
```

Or pass as parameter:
```python
generator = AdaptiveApplicationGenerator(region="us-east-1")
# The model is configurable in bedrock_client.py
```

## 🎓 How It Works

### Generation Process

1. **Requirements Analysis**: Parses your application requirements
2. **Specification Generation**: Claude generates detailed application specification (JSON)
3. **Project Structure Creation**: Creates organized directory layout
4. **Code Generation**: Generates main application files with Claude
5. **Configuration**: Creates config files and dependency lists
6. **Test Generation** (optional): Creates test files for verification
7. **Specification Export**: Saves the generated specification for reference

### What Gets Generated

- ✅ Main application code
- ✅ Configuration files
- ✅ Dependency manifests (requirements.txt, package.json)
- ✅ Project structure (src/, config/, tests/)
- ✅ Test files (if enabled)
- ✅ Application specification (JSON)

## 📊 Example Output

```
generated_apps/
└── my_task_api/
    ├── src/
    │   ├── __init__.py
    │   └── main.py                    # Generated main application
    ├── config/
    │   ├── __init__.py
    │   └── config.py                  # Generated configuration
    ├── tests/
    │   ├── __init__.py
    │   └── test_main.py               # Generated tests
    ├── requirements.txt               # Generated dependencies
    ├── APP_SPECIFICATION.json         # Generated specification
    └── [other generated files]
```

## 🔍 Troubleshooting

### AWS Bedrock Access Error
- Ensure AWS credentials are configured: `aws configure`
- Check region has Bedrock enabled
- Verify IAM permissions for bedrock-runtime

### Import Errors
- Ensure you're running from the project root directory
- Install dependencies: `pip3 install -r requirements.txt`
- Verify Python 3.9+ is being used

### Generation Errors
- Check that requirements are descriptive enough
- Ensure AWS credentials are valid
- Check AWS Bedrock quota/rate limits

## 🚀 Advanced Usage

### Custom Output Directory
```bash
python3 cli.py \
  --name my_app \
  --requirements "My app requirements" \
  --output-dir /path/to/custom/dir
```

### Skip Tests
```bash
python3 cli.py \
  --name my_app \
  --requirements "My app requirements" \
  --no-tests
```

### Specify AWS Region
```bash
python3 cli.py \
  --name my_app \
  --requirements "My app requirements" \
  --region us-west-2
```

## 📚 API Reference

### AdaptiveApplicationGenerator

```python
generator = AdaptiveApplicationGenerator(
    output_dir: str = "./generated_apps",
    region: str = "us-east-1"
)

result = generator.generate_application(
    requirements: str,           # Application requirements
    app_name: str,              # Name of the app
    app_type: str = "web",      # Type of app
    tech_stack: str = "python", # Technology stack
    include_tests: bool = True  # Generate tests
)
```

## 🤝 Contributing

Contributions are welcome! Some areas for enhancement:
- Additional tech stacks (Go, Rust, Java, etc.)
- More sophisticated application types
- Improved code generation templates
- Database schema generation
- API documentation generation
- Docker support

## 📄 License

This project demonstrates adaptive application generation using AWS Bedrock and is provided as-is.

## 🔗 Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Claude API Documentation](https://docs.anthropic.com/)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/configure-quickstart.html)

## 💡 Use Cases

- **Rapid Prototyping**: Quickly generate project structure for new ideas
- **Learning Tool**: Study AI-generated code patterns and best practices
- **Project Templates**: Bootstrap new projects with full structure
- **Technology Exploration**: Try new tech stacks without manual setup
- **Team Onboarding**: Generate consistent project structures for teams
- **Proof of Concepts**: Rapidly build POCs for client presentations

---

**Built with ❤️ using AWS Bedrock and Claude AI**
