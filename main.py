from fastapi import FastAPI, UploadFile, File
from db import resumes_collection
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"error": "Only PDFs are supported"}
    
    contents = await file.read()

    with open(file.filename, "wb") as f:
        f.write(contents)

    # Extract text using pdfplumber
    with pdfplumber.open(file.filename) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Store in MongoDB
    resume_data = {
        "filename": file.filename,
        "content": text
    }
    existing = resumes_collection.find_one({"filename": file.filename})
    if existing:
         return {"message": f"Resume '{file.filename}' already exists in DB!"}

    resumes_collection.insert_one(resume_data)

    return {"message": f"Resume '{file.filename}' uploaded and stored in DB!"}

@app.post("/upload_jd")
async def upload_jd(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            text = "".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file.filename.endswith(".txt"):
        text = await file.read()
        text = text.decode("utf-8")
    else:
        return {"error": "Unsupported file format. Use .pdf or .txt"}

    # Preview only for now
    return {
        "message": f"JD '{file.filename}' uploaded!",
        "jd_text_preview": text[:500]
    }

@app.post("/rank_resumes")
async def rank_resumes(file: UploadFile = File(...)):
    # Extract JD text from uploaded file
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            jd_text = "".join(page.extract_text() or "" for page in pdf.pages)
    elif file.filename.endswith(".txt"):
        jd_text = await file.read()
        jd_text = jd_text.decode("utf-8")
    else:
        return {"error": "Unsupported file format. Use .pdf or .txt"}

    # Fetch all resumes from DB
    resumes = list(resumes_collection.find({}))
    if not resumes:
        return {"error": "No resumes found in the database"}

    resume_texts = [res["content"] for res in resumes]
    filenames = [res["filename"] for res in resumes]

    # Combine JD + resumes for TF-IDF
    documents = [jd_text] + resume_texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]

    # Calculate similarity scores
    similarity_scores = cosine_similarity(jd_vector, resume_vectors)[0]
    results = sorted(
        zip(filenames, similarity_scores),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "jd_filename": file.filename,
        "ranked_resumes": [
            {"filename": name, "score": round(score, 4)}
            for name, score in results
        ]
    }
