from __future__ import annotations

import html
import re
import unicodedata


def sanitize_text(text: str) -> str:

    replacements = {

        "\u2018": "'",
        "\u2019": "'",

        "\u201c": '"',
        "\u201d": '"',

        "\u2013": "-",
        "\u2014": "-",

        "\u2212": "-",

        "\u2026": "...",

        "\u00a0": " ",

        "\u2022": "-",

        "\ufeff": "",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    text = "".join(

        character

        for character in text

        if (
            character in "\n\r\t"
            or
            unicodedata.category(character) != "Cc"
        )
    )

    return text.strip()


def split_terms(
    terms: str
) -> list[str]:

    return [
        item.strip()

        for item in terms.split(";")

        if item.strip()
    ]


def safe_filename(
    value: str
) -> str:

    value = re.sub(

        r"[^A-Za-z0-9_-]+",

        "_",

        value.strip()
    )

    value = value.strip("_")

    return value or "legal_document"


def html_preview(
    text: str
) -> str:

    escaped = html.escape(
        sanitize_text(text)
    )

    blocks = []

    for line in escaped.splitlines():

        if not line.strip():

            blocks.append(
                "<div class='spacer'></div>"
            )

        elif (
            re.match(
                r"^\d+[.)]\s+",
                line
            )
            or
            (
                line.isupper()
                and len(line) < 100
            )
        ):

            blocks.append(
                f"<h4>{line}</h4>"
            )

        elif line.startswith("- "):

            blocks.append(
                f"<li>{line[2:]}</li>"
            )

        else:

            blocks.append(
                f"<p>{line}</p>"
            )

    return (
        "<div class='legal-card'>"
        + "".join(blocks)
        + "</div>"
    )