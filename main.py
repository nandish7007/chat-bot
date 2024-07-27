import os
import uvicorn
import numpy as np

from openai import OpenAI
from pypdf import PdfReader
from transformers import pipeline
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File, Form
from sklearn.feature_extraction.text import TfidfVectorizer


app = FastAPI()

pdf_text = ""
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
hf_pipeline = pipeline("text-generation", model="gpt2")


def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()

    return text


def get_relevant_text(query, text, top_n=5):
    vectorizer = TfidfVectorizer().fit_transform([query] + text)
    vectors = vectorizer.toarray()

    cosine_similarities = np.dot(vectors[0], vectors[1:].T)
    relevant_indices = cosine_similarities.argsort()[-top_n:][::-1]
    relevant_texts = [text[i] for i in relevant_indices]

    return " ".join(relevant_texts)


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_text
    pdf_text = extract_text_from_pdf(file.file)
    return {"message": "PDF uploaded and text extracted successfully"}


@app.post("/query/")
async def query_pdf(query: str = Form(...)):
    if not pdf_text:
        return JSONResponse(status_code=400, content={"message": "No PDF uploaded"})

    chunks = pdf_text.split("\n\n")
    relevant_text = get_relevant_text(query, chunks)
    if os.getenv("USE_OPENAI", "true") == "true":
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {relevant_text}\n\nQuestion: {query}\nAnswer:"}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message.content.strip()
    else:
        answer = hf_pipeline(f"Context: {relevant_text}\n\nQuestion: {query}\nAnswer:")[0]["generated_text"]

    return {"answer": answer}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
