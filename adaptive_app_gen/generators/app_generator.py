"""
Application generator for creating adaptive applications
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from adaptive_app_gen.bedrock_client import BedrockClient
from adaptive_app_gen.generators.java_generator import JavaProjectGenerator, JavaFileGenerator
from adaptive_app_gen.generators.python_generator import PythonProjectGenerator, PythonFileGenerator

logger = logging.getLogger(__name__)


class AdaptiveApplicationGenerator:
    """Generates complete adaptive applications using AWS Bedrock"""
    
    def __init__(self, output_dir: str = "./generated_apps", region: str = "us-east-1"):
        """
        Initialize the application generator
        
        Args:
            output_dir: Directory to output generated applications
            region: AWS region for Bedrock
        """
        self.output_dir = Path(output_dir)
        self.bedrock = BedrockClient(region=region)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized AdaptiveApplicationGenerator with output dir: {output_dir}")
    
    @staticmethod
    def _clean_code(code: str) -> str:
        """
        Remove markdown code block markers from generated code
        
        Args:
            code: Generated code that may contain markdown formatting
            
        Returns:
            Cleaned code without markdown markers
        """
        # Remove markdown code block markers
        if code.startswith('```'):
            # Find the language identifier line
            lines = code.split('\n')
            start_idx = 0
            
            # Skip opening markdown blocks
            while start_idx < len(lines) and lines[start_idx].strip().startswith('```'):
                start_idx += 1
                # Skip language identifier if present
                if start_idx < len(lines) and lines[start_idx].strip() in ['python', 'py', 'javascript', 'js', 'typescript', 'ts', 'java']:
                    start_idx += 1
            
            # Remove closing markdown block
            end_idx = len(lines)
            while end_idx > start_idx and lines[end_idx - 1].strip().startswith('```'):
                end_idx -= 1
            
            code = '\n'.join(lines[start_idx:end_idx])
        
        return code.strip()
    
    def generate_application(
        self,
        requirements: str,
        app_name: str,
        app_type: str = "web",
        tech_stack: str = "python",
        include_tests: bool = True,
    ) -> Dict[str, Any]:
        """
        Generate a complete adaptive application
        
        Args:
            requirements: Application requirements
            app_name: Name of the application
            app_type: Type of application (web, cli, api, etc.)
            tech_stack: Preferred tech stack (python, nodejs, typescript, etc.)
            include_tests: Whether to generate test files
            
        Returns:
            Dictionary with generation results and paths
        """
        logger.info(f"Starting generation of {app_name} ({app_type}, {tech_stack})")
        
        # Step 1: Generate specification
        logger.info("Step 1: Generating application specification...")
        spec = self.bedrock.generate_application_spec(
            requirements=requirements,
            app_type=app_type,
            tech_stack=tech_stack
        )
        spec["name"] = app_name
        
        # Step 2: Create project structure
        logger.info("Step 2: Creating project structure...")
        project_path = self.output_dir / app_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        self._create_project_structure(project_path, spec, tech_stack)
        
        # Step 3: Generate code files
        logger.info("Step 3: Generating code files...")
        generated_files = self._generate_code_files(project_path, spec, tech_stack)
        
        # Step 4: Generate configuration files
        logger.info("Step 4: Generating configuration files...")
        config_files = self._generate_config_files(project_path, spec, tech_stack)
        
        # Step 5: Generate tests (optional)
        if include_tests:
            logger.info("Step 5: Generating test files...")
            test_files = self._generate_test_files(project_path, spec, tech_stack)
            generated_files.update(test_files)
        
        # Step 6: Generate setup scripts and virtual environment
        logger.info("Step 6: Generating setup scripts...")
        setup_files = self._generate_setup_scripts(project_path, spec, tech_stack)
        generated_files.update(setup_files)
        
        # Step 7: Create virtual environment (Python only)
        if tech_stack.lower() in ["python", "py"]:
            logger.info("Step 7: Creating virtual environment...")
            venv_path = project_path / "venv"
            self._create_venv(venv_path)
        
        # Step 8: Save specification
        spec_path = project_path / "APP_SPECIFICATION.json"
        with open(spec_path, "w") as f:
            json.dump(spec, f, indent=2)
        
        result = {
            "success": True,
            "app_name": app_name,
            "project_path": str(project_path),
            "specification": spec,
            "generated_files": generated_files,
            "config_files": config_files,
        }
        
        logger.info(f"Successfully generated {app_name}")
        return result
    
    
    def _create_project_structure(self, project_path: Path, spec: Dict[str, Any], tech_stack: str) -> None:
        """Create the basic project directory structure"""
        tech_stack_lower = tech_stack.lower()
        directories = spec.get("project_structure", {}).get("directories", ["src", "tests", "config"])
        
        for directory in directories:
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Only create __init__.py for Python packages
            if tech_stack_lower in ["python", "py"]:
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
    
    def _generate_code_files(
        self,
        project_path: Path,
        spec: Dict[str, Any],
        tech_stack: str
    ) -> Dict[str, str]:
        """Generate main application code files"""
        generated_files = {}
        tech_stack_lower = tech_stack.lower()
        
        if tech_stack_lower in ["python", "py"]:
            generated_files["main.py"] = self._generate_python_main(project_path, spec)
            generated_files["config.py"] = self._generate_python_config(project_path, spec)
            
        elif tech_stack_lower in ["nodejs", "node", "javascript", "js"]:
            generated_files["main.js"] = self._generate_js_main(project_path, spec)
            generated_files["config.js"] = self._generate_js_config(project_path, spec)
            
        elif tech_stack_lower in ["typescript", "ts"]:
            generated_files["main.ts"] = self._generate_ts_main(project_path, spec)
            generated_files["config.ts"] = self._generate_ts_config(project_path, spec)
        
        elif tech_stack_lower in ["java"]:
            generated_files["Main.java"] = self._generate_java_main(project_path, spec)
            generated_files["Config.java"] = self._generate_java_config(project_path, spec)
        
        return generated_files
    
    def _generate_python_main(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate Python main file and package structure"""
        app_name = spec.get("name", "app").replace("-", "_")
        
        # Create package directory
        package_dir = project_path / app_name
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate __init__.py
        init_content = PythonFileGenerator.generate_main_module(spec)
        init_path = package_dir / "__init__.py"
        init_path.write_text(init_content)
        
        # Generate __main__.py (for python -m execution)
        main_entry_content = PythonFileGenerator.generate_main_entry_point(spec)
        main_entry_path = package_dir / "__main__.py"
        main_entry_path.write_text(main_entry_content)
        
        # Create src directory structure for imports
        src_dir = project_path / "src"
        src_dir.mkdir(exist_ok=True)
        
        # Create src/__init__.py
        src_init = src_dir / "__init__.py"
        src_init.write_text('"""Source code package"""\n')
        
        # Create API module
        api_dir = src_dir / "api"
        api_dir.mkdir(exist_ok=True)
        (api_dir / "__init__.py").write_text('"""API module"""\n')
        routes_content = PythonFileGenerator.generate_routes_module()
        (api_dir / "routes.py").write_text(routes_content)
        
        # Create middleware module
        middleware_dir = src_dir / "middleware"
        middleware_dir.mkdir(exist_ok=True)
        (middleware_dir / "__init__.py").write_text('"""Middleware module"""\n')
        jwt_middleware_content = PythonFileGenerator.generate_jwt_middleware_module()
        (middleware_dir / "jwt_middleware.py").write_text(jwt_middleware_content)
        
        # Create utils module
        utils_dir = src_dir / "utils"
        utils_dir.mkdir(exist_ok=True)
        (utils_dir / "__init__.py").write_text('"""Utilities module"""\n')
        exceptions_content = PythonFileGenerator.generate_exceptions_module()
        (utils_dir / "exceptions.py").write_text(exceptions_content)
        
        # Create models module
        models_dir = src_dir / "models"
        models_dir.mkdir(exist_ok=True)
        (models_dir / "__init__.py").write_text('"""Database models module"""\n')
        database_content = PythonFileGenerator.generate_database_module()
        (models_dir / "database.py").write_text(database_content)
        
        # Create core subdirectory
        core_dir = package_dir / "core"
        core_dir.mkdir(exist_ok=True)
        core_init = core_dir / "__init__.py"
        core_init.write_text('"""Core application functionality"""\n')
        
        # Generate utility modules that might be referenced by Bedrock-generated code
        self._generate_utility_modules(src_dir)
        
        # Generate main.py using static template (avoid Bedrock import mismatches)
        main_content = PythonFileGenerator.generate_fastapi_main(spec)
        main_path = package_dir / "main.py"
        main_path.write_text(main_content)
        
        return str(main_path)
    
    def _generate_utility_modules(self, src_dir: Path) -> None:
        """Generate comprehensive utility modules for common use cases"""
        utils_dir = src_dir / "utils"
        
        # Add logger module if not present
        logger_path = utils_dir / "logger.py"
        if not logger_path.exists():
            logger_content = PythonFileGenerator.generate_logger_module()
            logger_path.write_text(logger_content)
        
        # Add validators module if not present
        validators_path = utils_dir / "validators.py"
        if not validators_path.exists():
            validators_content = PythonFileGenerator.generate_validators_module()
            validators_path.write_text(validators_content)
        
        # Add helpers module if not present
        helpers_path = utils_dir / "helpers.py"
        if not helpers_path.exists():
            helpers_content = PythonFileGenerator.generate_helpers_module()
            helpers_path.write_text(helpers_content)
    
    def _generate_python_config(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate Python configuration file"""
        app_name = spec.get("name", "app").replace("-", "_")
        package_dir = project_path / app_name
        
        # Generate config module
        config_content = PythonFileGenerator.generate_config_module(spec)
        config_path = package_dir / "config.py"
        config_path.write_text(config_content)
        
        # Generate CLI module
        cli_content = PythonFileGenerator.generate_cli_module(spec)
        cli_path = package_dir / "cli.py"
        cli_path.write_text(cli_content)
        
        return str(config_path)
    
    def _generate_js_main(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate JavaScript main file"""
        code = self.bedrock.generate_code(spec, file_type="main.js")
        code = self._clean_code(code)
        main_path = project_path / "src" / "main.js"
        main_path.write_text(code)
        return str(main_path)
    
    def _generate_js_config(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate JavaScript configuration file"""
        code = self.bedrock.generate_code(spec, file_type="config.js")
        config_path = project_path / "config" / "config.js"
        config_path.write_text(code)
        return str(config_path)
    
    def _generate_ts_main(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate TypeScript main file"""
        code = self.bedrock.generate_code(spec, file_type="main.ts")
        main_path = project_path / "src" / "main.ts"
        main_path.write_text(code)
        return str(main_path)
    
    def _generate_ts_config(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate TypeScript configuration file"""
        code = self.bedrock.generate_code(spec, file_type="config.ts")
        config_path = project_path / "config" / "config.ts"
        config_path.write_text(code)
        return str(config_path)
    
    def _generate_java_main(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate Java main application file"""
        src_path = project_path / "src" / "main" / "java" / "com" / "app"
        src_path.mkdir(parents=True, exist_ok=True)
        
        # Generate main class using template
        main_code = JavaFileGenerator.generate_main_class(spec)
        main_path = src_path / "Application.java"
        main_path.write_text(main_code)
        
        # Generate controller
        controller_code = JavaFileGenerator.generate_controller_class(spec)
        controller_path = src_path / "MainController.java"
        controller_path.write_text(controller_code)
        
        return str(main_path)
    
    def _generate_java_config(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate Java configuration file"""
        src_path = project_path / "src" / "main" / "java" / "com" / "app" / "config"
        src_path.mkdir(parents=True, exist_ok=True)
        
        # Generate config class using template
        config_code = JavaFileGenerator.generate_config_class(spec)
        config_path = src_path / "AppConfig.java"
        config_path.write_text(config_code)
        
        return str(config_path)
    
    def _generate_config_files(
        self,
        project_path: Path,
        spec: Dict[str, Any],
        tech_stack: str
    ) -> Dict[str, str]:
        """Generate configuration files (requirements.txt, package.json, pom.xml, etc.)"""
        generated_files = {}
        tech_stack_lower = tech_stack.lower()
        
        if tech_stack_lower in ["python", "py"]:
            # Generate requirements.txt
            requirements_path = project_path / "requirements.txt"
            requirements_content = PythonProjectGenerator.generate_requirements_txt(spec)
            requirements_path.write_text(requirements_content)
            generated_files["requirements.txt"] = str(requirements_path)
            
            # Generate setup.py
            setup_py_path = project_path / "setup.py"
            setup_py_content = PythonProjectGenerator.generate_setup_py(spec)
            setup_py_path.write_text(setup_py_content)
            generated_files["setup.py"] = str(setup_py_path)
            
            # Generate pyproject.toml
            pyproject_path = project_path / "pyproject.toml"
            pyproject_content = PythonProjectGenerator.generate_pyproject_toml(spec)
            pyproject_path.write_text(pyproject_content)
            generated_files["pyproject.toml"] = str(pyproject_path)
            
            # Generate tox.ini
            tox_path = project_path / "tox.ini"
            tox_content = PythonProjectGenerator.generate_tox_ini(spec)
            tox_path.write_text(tox_content)
            generated_files["tox.ini"] = str(tox_path)
            
            # Generate .gitignore
            gitignore_path = project_path / ".gitignore"
            gitignore_content = PythonProjectGenerator.generate_gitignore()
            gitignore_path.write_text(gitignore_content)
            generated_files[".gitignore"] = str(gitignore_path)
            
        elif tech_stack_lower in ["nodejs", "node", "javascript", "js", "typescript", "ts"]:
            package_json_path = project_path / "package.json"
            package_json = {
                "name": spec.get("name", "app"),
                "version": "1.0.0",
                "description": spec.get("description", ""),
                "main": spec.get("entry_point", "src/main.js"),
                "dependencies": {}
            }
            
            for dep in spec.get("dependencies", []):
                package_json["dependencies"][dep] = "latest"
            
            import json as json_lib
            package_json_path.write_text(json_lib.dumps(package_json, indent=2))
            generated_files["package.json"] = str(package_json_path)
        
        elif tech_stack_lower in ["java"]:
            # Generate pom.xml
            pom_xml_path = project_path / "pom.xml"
            pom_xml_content = JavaProjectGenerator.generate_pom_xml(spec)
            pom_xml_path.write_text(pom_xml_content)
            generated_files["pom.xml"] = str(pom_xml_path)
            
            # Generate application.properties
            resources_path = project_path / "src" / "main" / "resources"
            resources_path.mkdir(parents=True, exist_ok=True)
            props_path = resources_path / "application.properties"
            props_content = JavaProjectGenerator.generate_application_properties(spec)
            props_path.write_text(props_content)
            generated_files["application.properties"] = str(props_path)
        
        return generated_files
    
    def _generate_test_files(
        self,
        project_path: Path,
        spec: Dict[str, Any],
        tech_stack: str
    ) -> Dict[str, str]:
        """Generate test files"""
        generated_files = {}
        tech_stack_lower = tech_stack.lower()
        
        if tech_stack_lower in ["python", "py"]:
            # Generate unit test
            test_code = PythonFileGenerator.generate_test_file(spec)
            test_path = project_path / "tests" / "test_main.py"
            test_path.parent.mkdir(parents=True, exist_ok=True)
            test_path.write_text(test_code)
            generated_files["test_main.py"] = str(test_path)
            
            # Create __init__.py in tests directory
            tests_init = test_path.parent / "__init__.py"
            tests_init.write_text('"""Test suite"""\n')
            
        elif tech_stack_lower in ["nodejs", "node", "javascript", "js", "typescript", "ts"]:
            test_code = self.bedrock.generate_code(spec, file_type="main.test.js")
            test_path = project_path / "tests" / "main.test.js"
            test_path.parent.mkdir(parents=True, exist_ok=True)
            test_path.write_text(test_code)
            generated_files["main.test.js"] = str(test_path)
        
        elif tech_stack_lower in ["java"]:
            # Generate JUnit test
            test_code = JavaFileGenerator.generate_test_class(spec)
            test_path = project_path / "src" / "test" / "java" / "com" / "app" / "AppTest.java"
            test_path.parent.mkdir(parents=True, exist_ok=True)
            test_path.write_text(test_code)
            generated_files["AppTest.java"] = str(test_path)
        
        return generated_files
    
    def _generate_setup_scripts(
        self,
        project_path: Path,
        spec: Dict[str, Any],
        tech_stack: str
    ) -> Dict[str, str]:
        """Generate setup scripts for environment initialization"""
        generated_files = {}
        tech_stack_lower = tech_stack.lower()
        app_name = spec.get("name", "app").replace("-", "_")
        
        if tech_stack_lower in ["python", "py"]:
            # Create setup.sh for macOS/Linux
            setup_sh = f'''#!/bin/bash
# Setup script for {app_name}
# Creates and activates virtual environment, installs dependencies

set -e

echo "Setting up {app_name}..."

# Check Python version
python3 --version || {{ echo "Error: Python 3 is not installed"; exit 1; }}

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the application:"
echo "  python -m {app_name}"
echo ""
'''
            setup_sh_path = project_path / "setup.sh"
            setup_sh_path.write_text(setup_sh)
            setup_sh_path.chmod(0o755)  # Make executable
            generated_files["setup.sh"] = str(setup_sh_path)
            
            # Create setup.bat for Windows
            setup_bat = f'''@echo off
REM Setup script for {app_name}
REM Creates and activates virtual environment, installs dependencies

echo Setting up {app_name}...

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\\Scripts\\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

echo.
echo ✅ Setup complete!
echo.
echo To activate the virtual environment, run:
echo   venv\\Scripts\\activate.bat
echo.
echo To run the application:
echo   python -m {app_name}
echo.
pause
'''
            setup_bat_path = project_path / "setup.bat"
            setup_bat_path.write_text(setup_bat)
            generated_files["setup.bat"] = str(setup_bat_path)
            
            # Create SETUP.md with instructions
            setup_md = f'''# Setup Instructions for {app_name}

## Quick Start (Automated)

### macOS/Linux
```bash
./setup.sh
source venv/bin/activate
```

### Windows
```cmd
setup.bat
```

## Manual Setup

### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 2: Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\\Scripts\\activate.bat
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python -m {app_name}
```

## Virtual Environment

A virtual environment is already created in the `venv` folder. This ensures all dependencies are isolated from your system Python.

### Deactivate Virtual Environment
```bash
deactivate
```

### Remove Virtual Environment (if needed)
```bash
rm -rf venv  # macOS/Linux
rmdir venv   # Windows
```

## Troubleshooting

**Python not found:** Make sure Python 3.9+ is installed and in your PATH
```bash
python3 --version
```

**Permission denied on setup.sh:** Make it executable
```bash
chmod +x setup.sh
```

**Virtual environment issues:** Delete and recreate
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
'''
            setup_md_path = project_path / "SETUP.md"
            setup_md_path.write_text(setup_md)
            generated_files["SETUP.md"] = str(setup_md_path)
        
        elif tech_stack_lower in ["nodejs", "node", "javascript", "js", "typescript", "ts"]:
            # Create setup.sh for npm
            setup_sh = f'''#!/bin/bash
# Setup script for {app_name}
# Installs Node.js dependencies

set -e

echo "Setting up {app_name}..."

# Check Node.js version
node --version || {{ echo "Error: Node.js is not installed"; exit 1; }}

# Install dependencies
if [ -f "package.json" ]; then
    echo "Installing dependencies from package.json..."
    npm install
else
    echo "package.json not found"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  npm start"
echo ""
'''
            setup_sh_path = project_path / "setup.sh"
            setup_sh_path.write_text(setup_sh)
            setup_sh_path.chmod(0o755)
            generated_files["setup.sh"] = str(setup_sh_path)
            
            # Create setup.bat for Windows
            setup_bat = f'''@echo off
REM Setup script for {app_name}
REM Installs Node.js dependencies

echo Setting up {app_name}...

REM Check Node.js version
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    exit /b 1
)

REM Install dependencies
if exist "package.json" (
    echo Installing dependencies from package.json...
    npm install
) else (
    echo package.json not found
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo To run the application:
echo   npm start
echo.
pause
'''
            setup_bat_path = project_path / "setup.bat"
            setup_bat_path.write_text(setup_bat)
            generated_files["setup.bat"] = str(setup_bat_path)
        
        return generated_files
    
    def _create_venv(self, venv_path: Path) -> None:
        """Create a Python virtual environment"""
        import subprocess
        import sys
        
        try:
            logger.info(f"Creating virtual environment at {venv_path}...")
            subprocess.run(
                [sys.executable, "-m", "venv", str(venv_path)],
                check=True,
                capture_output=True
            )
            logger.info("Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to create virtual environment: {e}")
            logger.info("Virtual environment creation is optional - you can create it manually")
