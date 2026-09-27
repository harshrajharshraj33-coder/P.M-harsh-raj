from __future__ import annotations

from io import BytesIO
from pathlib import Path

from docx import Document

from docx.enum.paragraph import WD_ALIGN_PARAGRAPH

from docx.enum.table import WD_TABLE_ALIGNMENT

from docx.shared import Inches, Pt

from backend.document_generators.text_utils import (
    sanitize_text
)


LOGO_PATH = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "legal_ease_logo.png"
)


def format_docx(
    text: str,
    doc_type: str,
    company_name: str = "LegalEase"
) -> bytes:

    document = Document()

    section = document.sections[0]

    section.top_margin = Inches(0.75)

    section.bottom_margin = Inches(0.75)

    section.left_margin = Inches(0.85)

    section.right_margin = Inches(0.85)

    normal = document.styles["Normal"]

    normal.font.name = "Times New Roman"

    normal.font.size = Pt(11)

    # Logo
    if LOGO_PATH.exists():

        paragraph = document.add_paragraph()

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )

        paragraph.add_run().add_picture(

            str(LOGO_PATH),

            width=Inches(1.2)
        )

    # Document title
    title = document.add_paragraph()

    title.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    run = title.add_run(
        sanitize_text(doc_type).upper()
    )

    run.bold = True

    run.font.name = "Times New Roman"

    run.font.size = Pt(16)

    # Main content
    for raw_line in sanitize_text(text).splitlines():

        line = raw_line.strip()

        if not line:

            document.add_paragraph()

            continue

        if (
            line.isupper()
            and len(line) <= 100
        ):

            paragraph = document.add_paragraph()

            run = paragraph.add_run(line)

            run.bold = True

            run.font.name = "Times New Roman"

            run.font.size = Pt(12)

        elif line.startswith(
            ("- ", "* ")
        ):

            document.add_paragraph(

                line[2:],

                style="List Bullet"
            )

        else:

            document.add_paragraph(
                line
            )

    # Footer
    footer = section.footer.paragraphs[0]

    footer.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    footer_run = footer.add_run(

        f"{company_name} | "
        "AI-generated draft - review before use"
    )

    footer_run.italic = True

    # Terms/status table
    table = document.add_table(
        rows=1,
        cols=2
    )

    table.alignment = (
        WD_TABLE_ALIGNMENT.CENTER
    )

    table.style = "Table Grid"

    table.cell(0, 0).text = "Document"

    table.cell(0, 1).text = "Status"

    row = table.add_row().cells

    row[0].text = sanitize_text(
        doc_type
    )

    row[1].text = "Draft for review"

    output = BytesIO()

    document.save(output)

    return output.getvalue()