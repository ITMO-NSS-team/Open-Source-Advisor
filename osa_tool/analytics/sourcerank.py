import os
import re
from typing import Union
from functools import lru_cache
from gitingest import ingest

from osa_tool.readmeai.config.settings import ConfigLoader
from osa_tool.readmeai.readmegen_article.config.settings import ArticleConfigLoader
from osa_tool.utils import parse_folder_name
from osa_tool.analytics.metadata import load_data_metadata


class SourceRank:

    def __init__(
            self,
            config_loader: Union[ConfigLoader, ArticleConfigLoader]
    ):
        self.config = config_loader.config
        self.repo_url = self.config.git.repository
        self.metadata = load_data_metadata(self.repo_url)
        self.repo_path = os.path.join(os.getcwd(), parse_folder_name(self.repo_url))
        self.summary, self.tree, self.content = ingest(self.repo_path)

    def readme_presence(self) -> bool:
        pattern = re.compile(r'\bREADME(\.\w+)?\b', re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def license_presence(self) -> bool:
        pattern = re.compile(r'\bLICEN[SC]E(\.\w+)?\b', re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def examples_presence(self) -> bool:
        pattern = re.compile(r'\b(tutorials?|examples|notebooks?)\b',
                             re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def docs_presence(self) -> bool:
        pattern = re.compile(r'\b(docs?|documentation|wiki|manuals?)\b',
                             re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def print_results(self) -> None:
        print(self.readme_presence())
        print(self.license_presence())
        print(self.examples_presence())
        print(self.docs_presence())


