from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator
)

from backend.config import get_settings

from backend.schemas import (
    DocumentRequest,
    DocumentResponse
)


router = APIRouter()

generator = GeminiDocumentGenerator()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        content = generator.generate_document(
            request
        )

        settings = get_settings()

        return DocumentResponse(

            document_type=request.document_type,

            content=content,

            model=settings.gemini_model,

            demo_mode=settings.demo_mode,
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected generation error: {exc}"
        ) from exc