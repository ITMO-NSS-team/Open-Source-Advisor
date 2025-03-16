import logging
import os
import tomli as tomllib
from typing import Union
from datetime import datetime

import qrcode
from rich.logging import RichHandler

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)

from osa_tool.analytics.metadata import load_data_metadata
from osa_tool.analytics.sourcerank import SourceRank
from osa_tool.readmeai.config.settings import ConfigLoader
from osa_tool.readmeai.readmegen_article.config.settings import \
    ArticleConfigLoader
from osa_tool.osatreesitter.models import ModelHandlerFactory, ModelHandler
from osa_tool.utils import parse_folder_name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

logger = logging.getLogger("rich")


class ReportGenerator:
    def __init__(self,
                 config_loader: Union[ConfigLoader, ArticleConfigLoader]):
        self.config = config_loader.config
        self.sourcerank = SourceRank(config_loader)
        self.text_generator = TextGenerator(config_loader)
        self.repo_url = self.config.git.repository
        self.osa_url = "https://github.com/ITMO-NSS-team/Open-Source-Advisor"
        self.metadata = load_data_metadata(self.repo_url)

        self.logo_path = os.path.join(
            os.getcwd(),
            "docs",
            "images",
            "osa_logo.PNG"
        )
        self.output_path = os.path.join(
            os.getcwd(),
            "examples",
            f"{self.metadata.name}_report.pdf"
        )

    @staticmethod
    def table_builder(
            data,
            w_first_col,
            w_second_col,
            coloring=False,
    ) -> Table:
        table = Table(data, colWidths=[w_first_col, w_second_col])
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFCCFF")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
        if coloring:
            for row_idx, row in enumerate(data[1:], start=1):
                value = row[1]
                bg_color = colors.lightgreen if value == "✓" else colors.lightcoral
                style.append(("BACKGROUND", (1, row_idx), (1, row_idx), bg_color))

        table.setStyle(TableStyle(style))
        return table

    def generate_qr_code(self) -> str:
        qr = qrcode.make(self.osa_url)
        qr_path = os.path.join(os.getcwd(), "temp_qr.png")
        qr.save(qr_path)
        return qr_path

    def draw_images_and_tables(self, canvas_obj, doc) -> None:
        # Logo OSA
        canvas_obj.drawImage(self.logo_path, 335, 700, width=130, height=120)
        canvas_obj.linkURL(self.osa_url, (335, 700, 465, 820), relative=0)

        # QR OSA
        qr_path = self.generate_qr_code()
        canvas_obj.drawImage(qr_path, 450, 707, width=100, height=100)
        canvas_obj.linkURL(self.osa_url, (450, 707, 550, 807), relative=0)
        os.remove(qr_path)

        # Lines
        canvas_obj.setStrokeColor(colors.black)
        canvas_obj.setLineWidth(1.5)
        canvas_obj.line(30, 705, 570, 705)
        canvas_obj.line(30, 525, 570, 525)

        # Tables
        table1, table2 = self.table_generator()

        table1.wrapOn(canvas_obj, 0, 0)
        table1.drawOn(canvas_obj, 64, 540)

        table2.wrapOn(canvas_obj, 0, 0)
        table2.drawOn(canvas_obj, 286, 540)

    def header(self) -> list:
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name="LeftAligned",
            parent=styles["Title"],
            alignment=0,
            leftIndent=-20,
        )
        title_line1 = Paragraph(f"Repository Analysis Report", title_style)
        title_line2 = Paragraph(f"for <a href='{self.repo_url}' color='#00008B'>{self.metadata.name}</a>", title_style)

        elements = [title_line1, title_line2]
        return elements

    def table_generator(self) -> tuple[Table, Table]:
        styles = getSampleStyleSheet()
        normal_style = ParagraphStyle(
            name="LeftAlignedNormal",
            parent=styles["Normal"],
            fontSize=12,
            alignment=1,
        )
        data1 = [
            [Paragraph("<b>Statistics</b>", normal_style), Paragraph("<b>Values</b>", normal_style)],
            ["Stars Count", str(self.metadata.stars_count)],
            ["Watchers Count", str(self.metadata.watchers_count)],
            ["Forks Count", str(self.metadata.forks_count)],
            ["Issues Count", str(self.metadata.open_issues_count)],
        ]
        data2 = [
            [Paragraph("<b>Metric</b>", normal_style), Paragraph("<b>Values</b>", normal_style)],
            ["README Presence", "✓" if self.sourcerank.readme_presence() else "✗"],
            ["License Presence", "✓" if self.sourcerank.license_presence() else "✗"],
            ["Documentation Presence", "✓" if self.sourcerank.docs_presence() else "✗"],
            ["Examples Presence", "✓" if self.sourcerank.examples_presence() else "✗"],
            ["Tests Presence", "✓" if self.sourcerank.tests_presence() else "✗"],
            ["Description Presence", "✓" if self.metadata.description else "✗"],
        ]
        table1 = self.table_builder(data1, 120, 76)
        table2 = self.table_builder(data2, 160, 76, True)
        return table1, table2

    def body_first_part(self) -> ListFlowable:
        styles = getSampleStyleSheet()
        normal_style = ParagraphStyle(
            name="LeftAlignedNormal",
            parent=styles["Normal"],
            fontSize=12,
            leading=16,
            alignment=0,
        )
        repo_link = Paragraph(f"Repository Name: <a href='{self.repo_url}' color='#00008B'>{self.metadata.name}</a>", normal_style)
        owner_link = Paragraph(f"Owner: <a href='{self.metadata.owner_url}' color='#00008B'>{self.metadata.owner}</a>", normal_style)
        created_at = Paragraph(f"Created at: {datetime.strptime(self.metadata.created_at,'%Y-%m-%dT%H:%M:%SZ').strftime('%d.%m.%Y %H:%M')}", normal_style)

        bullet_list = ListFlowable(
            [
                ListItem(repo_link, leftIndent=14),
                ListItem(owner_link, leftIndent=14),
                ListItem(created_at, leftIndent=14),
            ],
            bulletType="bullet"
        )
        return bullet_list

    def body_second_part(self):
        styles = getSampleStyleSheet()
        normal_style = ParagraphStyle(
            name="LeftAlignedNormal",
            parent=styles["Normal"],
            fontSize=12,
            leading=13,
            spaceAfter=13,
            leftIndent=-20,
            rightIndent=-20,
            alignment=0,
        )
        text_content = self.text_generator.make_request()
        paragraphs = text_content.split("\n")

        story = []
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), normal_style))
        return story

    def build_pdf(self) -> None:
        logger.info(f"Starting analysis for repository {self.metadata.full_name}")

        try:
            doc = SimpleDocTemplate(self.output_path,
                                    pagesize=A4,
                                    topMargin=50,
                                    bottomMargin=40,
                                    leftMaring=10
                                    )
            doc.build(
                [
                    *self.header(),
                    Spacer(0, 40),
                    self.body_first_part(),
                    Spacer(0, 125),
                    *self.body_second_part(),
                ],
                onFirstPage=self.draw_images_and_tables,
            )
            logger.info(f"PDF report successfully created in {self.output_path}")
        except Exception as e:
            logger.error("Error while building PDF report, %s", e,
                         exc_info=True)


class TextGenerator:
    def __init__(self,
                 config_loader: Union[ConfigLoader, ArticleConfigLoader]):
        self.config = config_loader.config
        self.sourcerank = SourceRank(config_loader)
        self.model_handler: ModelHandler = ModelHandlerFactory.build(
            self.config)
        self.repo_url = self.config.git.repository
        self.metadata = load_data_metadata(self.repo_url)
        self.base_path = os.path.join(os.getcwd(), parse_folder_name(self.repo_url))
        self.prompt_path = os.path.join(
            os.getcwd(),
            "osa_tool",
            "config",
            "standart",
            "settings",
            "prompt_for_analysis.toml"
        )

    def make_request(self) -> str:
        response = self.model_handler.send_request(self._build_prompt())
        return response

    def _build_prompt(self):
        with open(self.prompt_path, "rb") as f:
            prompts = tomllib.load(f)

        values = {
            "project_name": self.metadata.name,
            "metadata": self.metadata,
            "repository_tree": self.sourcerank.tree,
            "presence_files": self._extract_presence_files(),
            "readme_content": self._extract_readme_content(),
        }
        main_prompt = prompts.get("prompt", {}).get("main_prompt", "")
        return main_prompt.format(**values)

    def _extract_readme_content(self) -> str:
        if not self.sourcerank.readme_presence():
            return "No README.md file"

        for file in ["README.md", "README.rst"]:
            readme_path = os.path.join(self.base_path, file)

            if os.path.exists(readme_path):
                with open(readme_path, "r", encoding="utf-8") as f:
                    return f.read()

    def _extract_presence_files(self) -> list[str]:
        contents = [
            f"README presence is {self.sourcerank.readme_presence()}",
            f"LICENSE presence is {self.sourcerank.license_presence()}",
            f"Examples presence is {self.sourcerank.examples_presence()}",
            f"Documentation presence is {self.sourcerank.docs_presence()}",
            f"Tests presence is {self.sourcerank.tests_presence()}",
        ]
        return contents
