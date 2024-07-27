from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_query_without_pdf():
    response = client.post("/query/", data={"query": "What is the content of the PDF?"})
    assert response.status_code == 400
    assert response.json() == {"message": "No PDF uploaded"}


def test_upload_pdf():
    with open("test.pdf", "rb") as pdf:
        response = client.post("/upload-pdf/", files={"file": pdf})

    assert response.status_code == 200
    assert response.json() == {"message": "PDF uploaded and text extracted successfully"}


def test_query_pdf():
    test_upload_pdf()

    response = client.post("/query/", data={"query": "What is the content of the PDF?"})
    assert response.status_code == 200
    assert "answer" in response.json()

