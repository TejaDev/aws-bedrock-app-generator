"""
Application generator for creating adaptive applications
"""

import os
import json
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
        
        self._create_project_structure(project_path, spec)
        
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
        
        # Step 6: Save specification
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
    
    def _create_project_structure(self, project_path: Path, spec: Dict[str, Any]) -> None:
        """Create the basic project directory structure"""
        directories = spec.get("project_structure", {}).get("directories", ["src", "tests", "config"])
        
        for directory in directories:
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            # Create __init__.py for Python packages
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
        
        # Generate main.py
        code = self.bedrock.generate_code(spec, file_type="main.py")
        main_path = package_dir / "main.py"
        main_path.write_text(code)
        
        # Create core subdirectory
        core_dir = package_dir / "core"
        core_dir.mkdir(exist_ok=True)
        core_init = core_dir / "__init__.py"
        core_init.write_text('"""Core application functionality"""\n')
        
        return str(main_path)
    
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
