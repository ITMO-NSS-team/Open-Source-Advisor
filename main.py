import os
import argparse
import logging
from rich.logging import RichHandler
from readmeai.config.settings import ConfigLoader, GitSettings
from readmeai.main import readme_generator
from OSA.github_agent.github_agent import GithubAgent
from OSA.utils import parse_folder_name
from OSA.osatreesitter.osa_treesitter import OSA_TreeSitter
from OSA.osatreesitter.docgen import DocGen

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

logger = logging.getLogger("rich")


def main():
    """Main function to generate a README.md file for a GitHub repository.

    Handles command-line arguments, clones the repository, creates and checks out a branch,
    generates the README.md file, and commits and pushes the changes.
    """
    # Create a command line argument parser
    parser = argparse.ArgumentParser(
        description="Generate README.md for a GitHub repository"
    )
    parser.add_argument("repo_url", type=str, help="URL of the GitHub repository")

    args = parser.parse_args()
    repo_url = args.repo_url

    try:
        # Initialize GitHub agent and perform operations
        github_agent = GithubAgent(repo_url)
        github_agent.star_repository()
        github_agent.clone_repository()
        github_agent.create_and_checkout_branch()
        generate_docstrings(repo_url)
        readme_agent(repo_url)
        github_agent.commit_and_push_changes()
        github_agent.create_pull_request()
        logger.info("All operations completed successfully.")
    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)


def readme_agent(repo_url: str) -> None:
    """Generates a README.md file for the specified GitHub repository.

    Args:
        repo_url: URL of the GitHub repository.

    Raises:
        Exception: If an error occurs during README.md generation.
    """
    logger.info("Started generating README.md. Processing the repository: %s", repo_url)

    try:
        # Load configurations and update repository URL
        config_loader = ConfigLoader(config_dir="OSA/config")
        config_loader.config.git = GitSettings(repository=repo_url)

        # Define output directory and ensure it exists
        output_dir = os.path.join(os.getcwd(), parse_folder_name(repo_url))
        os.makedirs(output_dir, exist_ok=True)
        file_to_save = os.path.join(output_dir, "README.md")

        # Generate README.md
        readme_generator(config_loader, file_to_save)

        logger.info("README.md successfully generated in folder: %s", output_dir)

    except Exception as e:
        logger.error("Error while generating: %s", repr(e), exc_info=True)


def generate_docstrings(repo_url: str) -> None:
    """Generates a docstrings for .py's classes and methods of the provided repository.

    Args:
        repo_url: URL of the GitHub repository.

    """
    try:
        ts = OSA_TreeSitter(os.path.basename(repo_url))
        res = ts.analyze_directory(ts.cwd)
        dg = DocGen()
        dg.process_python_file(res)

    except Exception as e:
        logger.error("Error while docstring generation: %s", repr(e), exc_info=True)


if __name__ == "__main__":
    main()
