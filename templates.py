#!/usr/bin/env python3
"""
Template generator for TableFlow ERP Metadata Generator project structure.
This script creates the directory structure and empty files.

Usage:
    python template.py [project_directory]

If project_directory is not specified, it defaults to ./tableflow-erp-generator
"""

import os
import sys
from pathlib import Path

# Project structure definition - updated with latest structure
PROJECT_STRUCTURE = {
    "config": [
        "__init__.py",
        "constants.py",
        "settings.py"
    ],
    "core": [
        "__init__.py",
        "data_analysis.py",
        "pipeline.py"
    ],
    "core/metadata": [
        "__init__.py",
        "module_generator.py",
        "table_generator.py",
        "dashboard_generator.py",
        "layout_manager.py"
                ],
    "services": [
        "__init__.py",
        "openai_client.py",
        "excel_service.py"
    ],
    "utils": [
        "__init__.py",
        "data_loaders.py",
        "excel_utils.py",
        "dropdown_manager.py",
        "sanitizers.py",
        "layout_calculator.py",  # New utility for layout calculations
        "attribute_generator.py"  # New utility for attribute generation
    ],
    "prompts": [
        "__init__.py",
        "module_prompts.py",
        "table_prompts.py",
        "dashboard_prompts.py",
        "analysis_prompts.py"
    ],
    "models": [
        "__init__.py",
        "base.py",
        "module.py",
        "table.py",
        "dashboard.py"
    ],
    "artifacts": [],             # Main artifacts directory
    "artifacts/inputs": [],      # For input Excel files
    "artifacts/outputs": [],     # Empty directory for generated output files
    "templates": [
        "__init__.py",
        "crm_generator.py"
    ],
    "": [  # Root directory files
        "main.py",
        "requirements.txt",
        "README.md",
        ".env.example"
    ]
}

# Sample .env.example content
ENV_EXAMPLE_CONTENT = """# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here

# OpenAI Model Selection
OPENAI_MODEL=gpt-4o-mini

# Temperature settings for different functions (0-1)
# Lower values = more deterministic outputs
OPENAI_TEMPERATURE_DEFAULT=0.3
OPENAI_TEMPERATURE_STRUCTURE=0
OPENAI_TEMPERATURE_MODULE=0.5
OPENAI_TEMPERATURE_TABLE=0.5
OPENAI_TEMPERATURE_DASHBOARD=0.3

# Token limits for different functions
OPENAI_MAX_TOKENS_DEFAULT=1024
OPENAI_MAX_TOKENS_STRUCTURE=16000
OPENAI_MAX_TOKENS_MODULE=4096
OPENAI_MAX_TOKENS_TABLE=8192
OPENAI_MAX_TOKENS_DASHBOARD=8192

# API retry settings
OPENAI_MAX_RETRIES=3
OPENAI_RETRY_BASE_WAIT=2

# Application settings
DEBUG=False
DEFAULT_SHEET_PREVIEW_ROWS=100
"""

# Sample requirements.txt content
REQUIREMENTS_CONTENT = """# Core dependencies
pandas==2.0.3
openpyxl==3.1.2
openai==1.3.0
python-dotenv==1.0.0
backoff==2.2.1
pathlib==1.0.1

# Excel processing
xlrd==2.0.1
xlsxwriter==3.1.2

# Logging and utilities
loguru==0.7.2
"""

def create_project_structure(base_dir):
    """
    Create the project directory structure with empty files.
    
    Args:
        base_dir (str): Base directory for the project
    """
    # Create base directory if it doesn't exist
    base_path = Path(base_dir)
    base_path.mkdir(exist_ok=True)
    
    # Create directories and empty files
    for directory, files in PROJECT_STRUCTURE.items():
        # Create directory
        dir_path = base_path / directory if directory else base_path
        dir_path.mkdir(exist_ok=True, parents=True)
        
        # Create empty files
        for file in files:
            file_path = dir_path / file
            
            # Handle special files with content
            if file == ".env.example":
                with open(file_path, 'w') as f:
                    f.write(ENV_EXAMPLE_CONTENT)
            elif file == "requirements.txt":
                with open(file_path, 'w') as f:
                    f.write(REQUIREMENTS_CONTENT)
            else:
                # Create empty file if it doesn't exist
                if not file_path.exists():
                    file_path.touch()
            
            print(f"Created file: {file_path}")

if __name__ == "__main__":
    # Get base directory from command line arguments or use default
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = "tableflow-erp-generator"
    
    # Create project structure
    create_project_structure(base_dir)
    print(f"\n✅ Project structure created in '{base_dir}'")
    print(f"\nTo get started:")
    print(f"  1. cd {base_dir}")
    print(f"  2. Create a virtual environment: python -m venv venv")
    print(f"  3. Activate it: source venv/bin/activate  (or venv\\Scripts\\activate on Windows)")
    print(f"  4. Install dependencies: pip install -r requirements.txt")
    print(f"  5. Copy .env.example to .env and add your OpenAI API key")