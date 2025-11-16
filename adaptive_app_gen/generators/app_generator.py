"""
Application generator for creating adaptive applications
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from adaptive_app_gen.bedrock_client import BedrockClient

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
        """Generate Python main file"""
        code = self.bedrock.generate_code(spec, file_type="main.py")
        main_path = project_path / "src" / "main.py"
        main_path.write_text(code)
        return str(main_path)
    
    def _generate_python_config(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate Python configuration file"""
        code = self.bedrock.generate_code(spec, file_type="config.py")
        config_path = project_path / "config" / "config.py"
        config_path.write_text(code)
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
        code = self.bedrock.generate_code(spec, file_type="Main.java")
        src_path = project_path / "src" / "main" / "java" / "com" / "app"
        src_path.mkdir(parents=True, exist_ok=True)
        main_path = src_path / "Main.java"
        main_path.write_text(code)
        return str(main_path)
    
    def _generate_java_config(self, project_path: Path, spec: Dict[str, Any]) -> str:
        """Generate Java configuration file"""
        code = self.bedrock.generate_code(spec, file_type="Config.java")
        src_path = project_path / "src" / "main" / "java" / "com" / "app" / "config"
        src_path.mkdir(parents=True, exist_ok=True)
        config_path = src_path / "Config.java"
        config_path.write_text(code)
        return str(config_path)
    
    def _generate_config_files(
        self,
        project_path: Path,
        spec: Dict[str, Any],
        tech_stack: str
    ) -> Dict[str, str]:
        """Generate configuration files (requirements.txt, package.json, etc.)"""
        generated_files = {}
        tech_stack_lower = tech_stack.lower()
        
        if tech_stack_lower in ["python", "py"]:
            requirements_path = project_path / "requirements.txt"
            dependencies = spec.get("dependencies", [])
            requirements_path.write_text("\n".join(dependencies))
            generated_files["requirements.txt"] = str(requirements_path)
            
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
            pom_xml_path = project_path / "pom.xml"
            pom_xml = self.bedrock.generate_code(spec, file_type="pom.xml")
            pom_xml_path.write_text(pom_xml)
            generated_files["pom.xml"] = str(pom_xml_path)
        
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
            test_code = self.bedrock.generate_code(spec, file_type="test_main.py")
            test_path = project_path / "tests" / "test_main.py"
            test_path.write_text(test_code)
            generated_files["test_main.py"] = str(test_path)
            
        elif tech_stack_lower in ["nodejs", "node", "javascript", "js", "typescript", "ts"]:
            test_code = self.bedrock.generate_code(spec, file_type="main.test.js")
            test_path = project_path / "tests" / "main.test.js"
            test_path.write_text(test_code)
            generated_files["main.test.js"] = str(test_path)
        
        elif tech_stack_lower in ["java"]:
            test_code = self.bedrock.generate_code(spec, file_type="MainTest.java")
            test_path = project_path / "src" / "test" / "java" / "com" / "app" / "MainTest.java"
            test_path.parent.mkdir(parents=True, exist_ok=True)
            test_path.write_text(test_code)
            generated_files["MainTest.java"] = str(test_path)
        
        return generated_files
