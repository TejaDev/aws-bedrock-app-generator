"""
Java/Spring Boot specific project generator
"""

from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class JavaProjectGenerator:
    """Generates production-ready Java/Spring Boot projects"""
    
    @staticmethod
    def get_project_structure(spec: Dict[str, Any]) -> Dict[str, str]:
        """Get standard Java Maven project structure"""
        return {
            "src/main/java/com/app": "Main source code",
            "src/main/java/com/app/config": "Configuration classes",
            "src/main/java/com/app/service": "Service layer",
            "src/main/java/com/app/controller": "REST controllers",
            "src/main/java/com/app/model": "Data models",
            "src/main/java/com/app/repository": "Data access layer",
            "src/main/resources": "Application resources",
            "src/test/java/com/app": "Test code",
            "target": "Build output (generated)",
        }
    
    @staticmethod
    def generate_pom_xml(spec: Dict[str, Any]) -> str:
        """Generate Maven pom.xml configuration"""
        app_name = spec.get("name", "app")
        description = spec.get("description", "")
        dependencies = spec.get("dependencies", [])
        
        # Map common dependency names to Maven artifacts
        maven_deps = JavaProjectGenerator._map_dependencies_to_maven(dependencies)
        
        deps_xml = ""
        for dep, version in maven_deps.items():
            deps_xml += f"""        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>{dep}</artifactId>
            <version>{version}</version>
        </dependency>
"""
        
        pom_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.app</groupId>
    <artifactId>{app_name}</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>{app_name}</name>
    <description>{description}</description>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.5</version>
        <relativePath/>
    </parent>

    <properties>
        <java.version>17</java.version>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Spring Boot Starter Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring Boot Starter Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- H2 Database (development/testing) -->
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Lombok for reducing boilerplate -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

{deps_xml}    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.10.1</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""
        return pom_template
    
    @staticmethod
    def generate_application_properties(spec: Dict[str, Any]) -> str:
        """Generate application.properties for Spring Boot"""
        app_name = spec.get("name", "app")
        app_type = spec.get("app_type", "api")
        
        properties = f"""# Spring Boot Application Properties
# Generated for {app_name}

spring.application.name={app_name}
server.port=8080
server.servlet.context-path=/api

# Logging Configuration
logging.level.root=INFO
logging.level.com.app=DEBUG

# JPA/Hibernate Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect

# Database Configuration (H2 for development)
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# H2 Console (for development)
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console

# Application Metadata
app.version=1.0.0
app.description={spec.get('description', '')}
app.type={app_type}
"""
        return properties
    
    @staticmethod
    def _map_dependencies_to_maven(dependencies: list) -> Dict[str, str]:
        """Map common dependency names to Maven artifact versions"""
        maven_mapping = {
            "jackson": ("jackson-databind", "2.15.2"),
            "lombok": ("lombok", "1.18.30"),
            "junit": ("junit", "4.13.2"),
            "mockito": ("mockito-core", "5.3.1"),
            "postgresql": ("postgresql", "42.6.0"),
            "mysql": ("mysql-connector-java", "8.0.33"),
            "redis": ("spring-boot-starter-data-redis", "3.1.5"),
        }
        
        result = {}
        for dep in dependencies:
            dep_lower = dep.lower()
            if dep_lower in maven_mapping:
                name, version = maven_mapping[dep_lower]
                result[name] = version
        
        return result


class JavaFileGenerator:
    """Generates individual Java files"""
    
    @staticmethod
    def generate_main_class(spec: Dict[str, Any]) -> str:
        """Generate Spring Boot main application class"""
        app_name = spec.get("name", "Application")
        
        # Capitalize app name for class
        class_name = "".join(word.capitalize() for word in app_name.split("_")).replace("-", "")
        
        main_class = f"""package com.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import lombok.extern.slf4j.Slf4j;

/**
 * Main Spring Boot Application Class
 * Generated application entry point
 */
@Slf4j
@SpringBootApplication
@ComponentScan(basePackages = {{"com.app"}})
public class {class_name}Application {{

    public static void main(String[] args) {{
        SpringApplication.run({class_name}Application.class, args);
        log.info("{class_name} application started successfully");
    }}
}}
"""
        return main_class
    
    @staticmethod
    def generate_config_class(spec: Dict[str, Any]) -> str:
        """Generate Spring Boot configuration class"""
        config_class = """package com.app.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Bean;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

/**
 * Application Configuration
 * Central configuration management for the application
 */
@Slf4j
@Configuration
@EnableConfigurationProperties(AppConfig.AppProperties.class)
public class AppConfig {

    /**
     * Application properties loaded from application.properties
     */
    @Data
    @ConfigurationProperties(prefix = "app")
    public static class AppProperties {
        private String version;
        private String description;
        private String type;

        public AppProperties() {
            log.info("AppProperties initialized");
        }
    }

    @Bean
    public AppProperties appProperties() {
        log.info("Registering AppProperties bean");
        return new AppProperties();
    }
}
"""
        return config_class
    
    @staticmethod
    def generate_controller_class(spec: Dict[str, Any]) -> str:
        """Generate Spring Boot REST controller"""
        app_name = spec.get("name", "app")
        
        controller_class = f"""package com.app.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import lombok.extern.slf4j.Slf4j;
import java.util.HashMap;
import java.util.Map;

/**
 * Main REST Controller
 * Handles HTTP requests for the {app_name} application
 */
@Slf4j
@RestController
@RequestMapping("/api")
public class MainController {{

    /**
     * Health check endpoint
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {{
        log.info("Health check endpoint called");
        Map<String, Object> response = new HashMap<>();
        response.put("status", "UP");
        response.put("message", "{app_name} is running");
        response.put("timestamp", System.currentTimeMillis());
        return ResponseEntity.ok(response);
    }}

    /**
     * Info endpoint
     */
    @GetMapping("/info")
    public ResponseEntity<Map<String, Object>> info() {{
        log.info("Info endpoint called");
        Map<String, Object> response = new HashMap<>();
        response.put("name", "{app_name}");
        response.put("version", "1.0.0");
        response.put("status", "active");
        return ResponseEntity.ok(response);
    }}

    /**
     * Echo endpoint for testing
     */
    @PostMapping("/echo")
    public ResponseEntity<Map<String, Object>> echo(@RequestBody Map<String, Object> payload) {{
        log.info("Echo endpoint called with payload: {{}}", payload);
        Map<String, Object> response = new HashMap<>();
        response.put("received", payload);
        response.put("timestamp", System.currentTimeMillis());
        return ResponseEntity.ok(response);
    }}
}}
"""
        return controller_class
    
    @staticmethod
    def generate_test_class(spec: Dict[str, Any]) -> str:
        """Generate JUnit test class"""
        app_name = spec.get("name", "Application")
        class_name = "".join(word.capitalize() for word in app_name.split("_")).replace("-", "")
        
        test_class = f"""package com.app;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Integration Tests for {class_name}Application
 */
@Slf4j
@SpringBootTest
@AutoConfigureMockMvc
public class {class_name}ApplicationTest {{

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void testContextLoads() {{
        log.info("Context loads test passed");
    }}

    @Test
    public void testHealthEndpoint() throws Exception {{
        log.info("Testing /api/health endpoint");
        mockMvc.perform(get("/api/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
    }}

    @Test
    public void testInfoEndpoint() throws Exception {{
        log.info("Testing /api/info endpoint");
        mockMvc.perform(get("/api/info"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").exists())
                .andExpect(jsonPath("$.version").value("1.0.0"));
    }}
}}
"""
        return test_class
