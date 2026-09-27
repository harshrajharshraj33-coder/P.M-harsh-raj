from __future__ import annotations

from backend.config import get_settings
from backend.schemas import DocumentRequest


SYSTEM_INSTRUCTION = """
You are LegalEase, an AI assistant for drafting legal-document templates.

Your job is to create a professional legal-document draft from the facts supplied
by the user.

IMPORTANT RULES:

1. Do not invent names.
2. Do not invent dates.
3. Do not invent amounts.
4. Do not invent addresses.
5. Do not invent obligations.
6. Do not invent governing law.
7. Do not invent jurisdiction-specific requirements.
8. If an important detail is missing, use:
   [TO BE COMPLETED]

Use professional and clear legal language.

Use clear headings and numbered clauses.

Include a signature section.

The result is a legal-document draft and should be reviewed by a qualified
legal professional before signing.

Do not provide legal advice.

Do not wrap the output in Markdown code fences.
"""


class GeminiDocumentGenerator:

    def __init__(self) -> None:
        self.settings = get_settings()

    def _demo_document(
        self,
        request: DocumentRequest
    ) -> str:

        terms = [
            term.strip()
            for term in request.terms.split(";")
            if term.strip()
        ]

        if terms:
            term_lines = "\n".join(
                f"{index}. {term}"
                for index, term in enumerate(terms, 1)
            )
        else:
            term_lines = "1. [TO BE COMPLETED]"

        document = f"""
{request.document_type.upper()}

PARTIES

{request.parties}

EFFECTIVE DATE

{request.effective_date}


1. PURPOSE

This draft sets out the principal terms provided by the parties for the
{request.document_type}.


2. AGREED TERMS

{term_lines}


3. CONFIDENTIALITY

The parties should specify any confidentiality obligations applicable
to the transaction.


4. TERMINATION

The parties should specify termination rights, notice periods, and any
applicable consequences.


5. GOVERNING LAW

[TO BE COMPLETED - specify the applicable jurisdiction and governing law.]


6. SIGNATURES

Party 1: ______________________________

Date: ______________________________


Party 2: ______________________________

Date: ______________________________


DRAFTING NOTICE

This document is an AI-generated draft based only on the information
supplied by the user.

It should be reviewed for completeness and jurisdiction-specific
requirements before use.
"""

        return document.strip()

    def generate_document(
        self,
        request: DocumentRequest
    ) -> str:

        # Demo mode allows testing without Gemini.
        if self.settings.demo_mode:
            return self._demo_document(request)

        if not self.settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Add it to .env or set DEMO_MODE=true."
            )

        try:
            from google import genai
            from google.genai import types

        except ImportError as exc:

            raise RuntimeError(
                "google-genai is not installed. "
                "Run: pip install -r requirements.txt"
            ) from exc

        try:

            client = genai.Client(
                api_key=self.settings.gemini_api_key
            )

        except Exception as exc:

            raise RuntimeError(
                f"Could not initialize Gemini client: {exc}"
            ) from exc

        prompt = f"""
Create a professional legal-document draft.

DOCUMENT TYPE:
{request.document_type}

PARTIES:
{request.parties}

TERMS AND CONDITIONS:
{request.terms}

EFFECTIVE DATE:
{request.effective_date}

DOCUMENT REQUIREMENTS:

- Use the supplied document type.
- Clearly identify the parties.
- Include the effective date.
- Include the supplied terms.
- Organize the document using numbered sections.
- Use professional legal language.
- Include appropriate placeholders for missing information.
- Include a signature section.
- Do not invent material facts.
- Do not wrap the response in Markdown code fences.

Return only the document draft.
"""

        try:

            response = client.models.generate_content(

                model=self.settings.gemini_model,

                contents=prompt,

                config=types.GenerateContentConfig(

                    system_instruction=SYSTEM_INSTRUCTION,

                    temperature=0.2,

                    max_output_tokens=8000,
                ),
            )

        except Exception as exc:

            raise RuntimeError(
                f"Gemini generation failed: {exc}"
            ) from exc

        text = getattr(response, "text", None)

        if not text or not text.strip():

            raise RuntimeError(
                "Gemini returned an empty document."
            )

        return text.strip()