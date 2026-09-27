from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

from backend.document_generators.text_utils import (
    sanitize_text
)


LOGO_PATH = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "legal_ease_logo.png"
)


class LegalPDF(FPDF):

    def __init__(
        self,
        company_name: str
    ):

        super().__init__(
            orientation="P",
            unit="mm",
            format="A4"
        )

        self.company_name = company_name

    def header(self):

        if LOGO_PATH.exists():

            try:

                self.image(
                    str(LOGO_PATH),
                    x=92,
                    y=8,
                    w=26
                )

                self.ln(20)

            except Exception:

                self.ln(8)

        else:

            self.ln(8)

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            "I",
            8
        )

        self.cell(

            0,
            8,

            (
                f"{self.company_name} | "
                "AI-generated draft - "
                "review before use | "
                f"Page {self.page_no()}"
            ),

            align="C"
        )


def format_pdf(
    text: str,
    doc_type: str,
    company_name: str = "LegalEase"
) -> bytes:

    pdf = LegalPDF(
        company_name
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=20
    )

    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        15
    )

    pdf.multi_cell(
        0,
        9,
        sanitize_text(
            doc_type
        ).upper(),
        align="C"
    )

    pdf.ln(4)

    for raw_line in sanitize_text(
        text
    ).splitlines():

        line = raw_line.strip()

        if not line:

            pdf.ln(4)

            continue

        if (
            line.isupper()
            and len(line) <= 100
        ):

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                0,
                7,
                line
            )

        elif line.startswith(
            ("- ", "* ")
        ):

            pdf.set_font(
                "Helvetica",
                "",
                10.5
            )

            pdf.multi_cell(
                0,
                6,
                "- " + line[2:]
            )

        else:

            pdf.set_font(
                "Helvetica",
                "",
                10.5
            )

            pdf.multi_cell(
                0,
                6,
                line
            )

    return bytes(
        pdf.output()
    )