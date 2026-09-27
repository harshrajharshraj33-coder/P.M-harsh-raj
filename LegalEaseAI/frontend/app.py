from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import requests
import streamlit as st

from dotenv import load_dotenv


load_dotenv()


APP_DIR = Path(
    __file__
).resolve().parents[1]


LOGO_PATH = (
    APP_DIR
    / "assets"
    / "legal_ease_logo.png"
)


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide"
)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    """
<style>

.main-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 800;
    margin-bottom: 0.1rem;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 1.5rem;
}

.legal-card {
    background: #111827;
    color: #f9fafb;
    border-radius: 14px;
    padding: 26px;
    max-height: 620px;
    overflow-y: auto;
    line-height: 1.65;
}

.legal-card h4 {
    color: #93c5fd;
    margin-top: 18px;
    margin-bottom: 6px;
}

.legal-card p {
    margin: 5px 0;
}

.legal-card .spacer {
    height: 8px;
}

.notice {
    padding: 12px 16px;
    border-radius: 10px;
    background: #f3f4f6;
    margin: 10px 0 18px;
}

</style>
""",
    unsafe_allow_html=True
)


# --------------------------------------------------
# Logo
# --------------------------------------------------

if LOGO_PATH.exists():

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.image(
            str(LOGO_PATH),
            width=120
        )


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
<div class="main-title">
LegalEase
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    """
<div class="subtitle">
AI-Powered Legal Document Generator
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    """
<div class="notice">
LegalEase creates editable legal-document drafts.
Review jurisdiction-specific requirements with a
qualified legal professional before signing.
</div>
""",
    unsafe_allow_html=True
)


# --------------------------------------------------
# Input Form
# --------------------------------------------------

with st.form(
    "document_form"
):

    col1, col2 = st.columns(2)

    with col1:

        document_type = st.text_input(
            "Document Type",
            placeholder="Freelance Work Contract"
        )

        parties = st.text_area(
            "Parties Involved",
            placeholder=(
                "Jane Doe (Service Provider), "
                "TechNova Inc. (Client)"
            ),
            height=120
        )

    with col2:

        effective_date = st.date_input(
            "Effective Date",
            value=date.today()
        )

        terms = st.text_area(
            "Terms & Conditions",
            placeholder=(
                "Payment within 30 days; "
                "Confidentiality must be maintained; "
                "Either party may terminate with 15 days notice"
            ),
            height=120
        )

    submitted = st.form_submit_button(
        "Generate Document",
        type="primary",
        use_container_width=True
    )


# --------------------------------------------------
# Generate document
# --------------------------------------------------

if submitted:

    if not document_type.strip():

        st.error(
            "Please enter the document type."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    else:

        payload = {

            "document_type":
                document_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                terms.strip(),

            "effective_date":
                effective_date.isoformat(),
        }

        with st.spinner(
            "Generating your document..."
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=120
                )

                if response.ok:

                    data = response.json()

                    st.session_state.document = (
                        data["content"]
                    )

                    st.session_state.document_type = (
                        data["document_type"]
                    )

                    st.session_state.model = (
                        data.get(
                            "model",
                            "configured Gemini model"
                        )
                    )

                    st.success(
                        "Document generated successfully."
                    )

                else:

                    try:

                        detail = response.json().get(
                            "detail",
                            response.text
                        )

                    except Exception:

                        detail = response.text

                    st.error(
                        f"Backend error "
                        f"({response.status_code}): "
                        f"{detail}"
                    )

            except requests.RequestException as exc:

                st.error(

                    "Could not reach the FastAPI backend. "
                    "Start the backend first.\n\n"
                    f"Details: {exc}"
                )


# --------------------------------------------------
# Document preview
# --------------------------------------------------

if "document" in st.session_state:

    st.divider()

    st.subheader(
        "Document Preview"
    )

    st.caption(
        f"Model: "
        f"{st.session_state.get(
            'model',
            'configured model'
        )}"
    )

    edit = st.checkbox(
        "Click to Edit Document"
    )

    if edit:

        edited = st.text_area(

            "Editable Document",

            value=st.session_state.document,

            height=620
        )

        st.session_state.document = edited

    else:

        from backend.document_generators.text_utils import (
            html_preview
        )

        st.markdown(
            html_preview(
                st.session_state.document
            ),
            unsafe_allow_html=True
        )


    # --------------------------------------------------
    # Downloads
    # --------------------------------------------------

    st.subheader(
        "Download"
    )

    from backend.document_generators.docx_generator import (
        format_docx
    )

    from backend.document_generators.pdf_generator import (
        format_pdf
    )

    from backend.document_generators.text_utils import (
        sanitize_text,
        safe_filename
    )


    text_bytes = (
        sanitize_text(
            st.session_state.document
        ).encode("utf-8")
    )


    docx_bytes = format_docx(

        st.session_state.document,

        st.session_state.document_type
    )


    pdf_bytes = format_pdf(

        st.session_state.document,

        st.session_state.document_type
    )


    base = safe_filename(

        st.session_state.document_type
    )


    d1, d2, d3 = st.columns(3)


    with d1:

        st.download_button(

            "Download TXT",

            text_bytes,

            file_name=f"{base}.txt",

            mime="text/plain",

            use_container_width=True
        )


    with d2:

        st.download_button(

            "Download DOCX",

            docx_bytes,

            file_name=f"{base}.docx",

            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            use_container_width=True
        )


    with d3:

        st.download_button(

            "Download PDF",

            pdf_bytes,

            file_name=f"{base}.pdf",

            mime="application/pdf",

            use_container_width=True
        )