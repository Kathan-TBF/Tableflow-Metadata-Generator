import os

def create_project_structure():
    """
    Creates a comprehensive directory structure for a Generative AI project 
    in the current directory.
    """
    # Configuration directory setup
    os.makedirs("config", exist_ok=True)
    
    config_files = {
        "__init__.py": "",
        "model_config.yaml": "# Model configuration settings",
        "prompt_templates.yaml": "# Prompt template configurations",
        "logging_config.yaml": "# Logging configuration settings"
    }
    
    for filename, content in config_files.items():
        with open(os.path.join("config", filename), "w") as f:
            f.write(content)

    # Source code directory setup
    os.makedirs("src", exist_ok=True)
    
    # LLM module
    os.makedirs(os.path.join("src", "llm"), exist_ok=True)
    
    llm_files = {
        "__init__.py": "",
        "base.py": "# Base LLM class definition",
        "claude_client.py": "# Claude API client implementation",
        "gpt_client.py": "# GPT API client implementation", 
        "utils.py": "# LLM-related utility functions"
    }
    
    for filename, content in llm_files.items():
        with open(os.path.join("src", "llm", filename), "w") as f:
            f.write(content)

    # Prompt Engineering module
    os.makedirs(os.path.join("src", "prompt_engineering"), exist_ok=True)
    
    prompt_eng_files = {
        "__init__.py": "",
        "templates.py": "# Prompt template management",
        "few_shot.py": "# Few-shot learning examples",
        "chain.py": "# Prompt chaining mechanisms"
    }
    
    for filename, content in prompt_eng_files.items():
        with open(os.path.join("src", "prompt_engineering", filename), "w") as f:
            f.write(content)

    # Utilities module
    os.makedirs(os.path.join("src", "utils"), exist_ok=True)
    
    utils_files = {
        "__init__.py": "",
        "rate_limiter.py": "# API rate limiting utilities",
        "token_counter.py": "# Token counting and management",
        "cache.py": "# Caching mechanisms",
        "logger.py": "# Custom logging utilities"
    }
    
    for filename, content in utils_files.items():
        with open(os.path.join("src", "utils", filename), "w") as f:
            f.write(content)

    # Handlers module
    os.makedirs(os.path.join("src", "handlers"), exist_ok=True)
    
    handlers_files = {
        "__init__.py": "",
        "error_handler.py": "# Centralized error handling"
    }
    
    for filename, content in handlers_files.items():
        with open(os.path.join("src", "handlers", filename), "w") as f:
            f.write(content)

    # Data directories
    data_subdirs = ["cache", "outputs", "prompts", "embeddings"]
    for subdir in data_subdirs:
        os.makedirs(os.path.join("data", subdir), exist_ok=True)

    # Examples directory
    os.makedirs("examples", exist_ok=True)
    
    example_files = {
        "basic_completion.py": "# Example of basic LLM completion",
        "chat_session.py": "# Example of managing a chat session",
        "chain_prompts.py": "# Example of chaining prompts"
    }
    
    for filename, content in example_files.items():
        with open(os.path.join("examples", filename), "w") as f:
            f.write(content)

    # Notebooks directory
    os.makedirs("notebooks", exist_ok=True)
    
    notebook_files = {
        "prompt_testing.ipynb": "# Notebook for testing prompts",
        "response_analysis.ipynb": "# Notebook for analyzing model responses",
        "model_experimentation.ipynb": "# Notebook for model experiments"
    }
    
    for filename, content in notebook_files.items():
        with open(os.path.join("notebooks", filename), "w") as f:
            f.write(content)

    # Root project files
    root_files = {
        "requirements.txt": "# Project dependencies",
        "setup.py": "# Project setup script",
        "README.md": "# Project documentation and overview",
        "Dockerfile": "# Docker configuration for project"
    }
    
    for filename, content in root_files.items():
        with open(filename, "w") as f:
            f.write(content)

    print("Project structure created in the current directory.")

if __name__ == "__main__":
    create_project_structure()