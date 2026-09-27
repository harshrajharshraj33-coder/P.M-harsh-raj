import os


# Use demo mode so tests do not need
# a real Gemini API key.

os.environ["DEMO_MODE"] = "true"

os.environ["GEMINI_API_KEY"] = ""


from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "LegalEase API is running"
    )


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_generate_demo_document():

    response = client.post(

        "/generate",

        json={

            "document_type":
                "NDA",

            "parties":
                (
                    "Alice (Disclosing Party), "
                    "Beta Ltd (Receiving Party)"
                ),

            "terms":
                (
                    "Confidentiality for 2 years; "
                    "No disclosure to third parties"
                ),

            "effective_date":
                "2026-10-01",
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert "NDA" in body["content"]

    assert (
        "Confidentiality for 2 years"
        in body["content"]
    )