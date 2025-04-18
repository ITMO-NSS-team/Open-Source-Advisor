import os
import logging
from rich.logging import RichHandler

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

logger = logging.getLogger("rich")

def add_github_actions_workflow(repo_url) -> None:
    """
    Creates a .github/workflows/ci.yml file with GitHub Actions configuration 
    in the local repository.
    
    Args:
        repo_url: URL of the GitHub repository.
    """
    try:
        repo_path = repo_url.rstrip("/").split("/")[-1]
        workflow_dir = os.path.join(repo_path, '.github', 'workflows')
        os.makedirs(workflow_dir, exist_ok=True)

        ci_yaml_path = os.path.join(workflow_dir, 'ci.yml')

        ci_yaml_content = """
name: CI

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

jobs:
  test-lint:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest

    - name: Run unit tests
      run: |
        PYTHONPATH=$PWD pytest
"""

        with open(ci_yaml_path, 'w', encoding='utf-8') as f:
            f.write(ci_yaml_content.strip() + '\n')
        
        logger.info("GitHub Actions workflow created successfully at %s", ci_yaml_path)

    except Exception as e:
        logger.error("Failed to create GitHub Actions workflow: %s", str(e))