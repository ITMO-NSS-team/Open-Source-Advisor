import os
import re

import tomli

from osa_tool.readmegen.utils import find_in_repo_tree
from osa_tool.utils import logger


class DependencyExtractor:
    """
    A utility class for extracting technology dependencies from common Python project files
    such as requirements.txt, pyproject.toml, and setup.py within a given repository.
    """
    def __init__(self, tree: str, base_path: str):
        self.tree = tree
        self.base_path = base_path

        # Regular expressions for matching dependencies in various files
        self.regex_requirements = r"^\s*([a-zA-Z0-9_\-]+)"
        self.regex_setup_install_requires = r"install_requires\s*=\s*\[([^]]+)]"
        self.regex_setup_dependency_items = r"'([^']+)'|\"([^\"]+)\""

    def extract_techs(self) -> set[str]:
        """
        Extracts a set of technologies used in the repository based on declared dependencies.

        Returns:
            set[str]: A set of technology names found in dependency files.
        """
        techs = set()

        techs.update(self._extract_from_requirements())
        techs.update(self._extract_from_pyproject())
        techs.update(self._extract_from_setup())

        return techs

    def _extract_from_requirements(self) -> set[str]:
        """
        Parses `requirements.txt` for listed dependencies.

        Returns:
            set[str]: A set of dependency names.
        """
        techs = set()
        rel_path = find_in_repo_tree(self.tree, r"requirements\.txt")
        if rel_path:
            abs_path = os.path.join(self.base_path, rel_path)
            if os.path.exists(abs_path):
                with open(abs_path, encoding="utf-8") as file:
                    for line in file:
                        match = re.match(self.regex_requirements, line)
                        if match:
                            techs.add(match.group(1).lower())
        return techs

    def _extract_from_pyproject(self) -> set[str]:
        """
        Parses `pyproject.toml` to extract dependencies from both PEP 621 and Poetry sections.

        Returns:
            set[str]: A set of dependency names.
        """
        techs = set()
        rel_path = find_in_repo_tree(self.tree, r"pyproject\.toml")
        if rel_path:
            abs_path = os.path.join(self.base_path, rel_path)
            if os.path.exists(abs_path):
                with open(abs_path, "rb") as f:
                    try:
                        data = tomli.load(f)

                        # PEP 621
                        deps = data.get("project", {}).get("dependencies", [])
                        techs.update(dep.split()[0].lower() for dep in deps)

                        # Poetry
                        poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
                        techs.update(name.lower() for name in poetry_deps.keys())

                    except tomli.TOMLDecodeError:
                        logger.error("Failed to decode pyproject.toml")
                        pass
        return techs

    def _extract_from_setup(self) -> set[str]:
        """
        Parses `setup.py` to extract dependencies listed in `install_requires`.

        Returns:
            set[str]: A set of dependency names.
        """
        techs = set()
        rel_path = find_in_repo_tree(self.tree, r"setup\.py")
        if rel_path:
            abs_path = os.path.join(self.base_path, rel_path)
            if os.path.exists(abs_path):
                with open(abs_path, encoding="utf-8") as f:
                    content = f.read()
                    match = re.search(self.regex_setup_install_requires, content, re.DOTALL)
                    if match:
                        items = re.findall(self.regex_setup_dependency_items, match.group(1))
                        for item in items:
                            dep = next(filter(None, item))
                            techs.add(dep.split()[0].lower())
        return techs
