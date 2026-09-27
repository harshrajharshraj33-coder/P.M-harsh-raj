from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=3000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "effective_date"
    )
    @classmethod
    def strip_values(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty")

        return value


class DocumentResponse(BaseModel):

    document_type: str

    content: str

    model: str

    demo_mode: bool