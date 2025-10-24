Smart Interview Scheduler
📌 Overview

The Smart Interview Scheduler is an intelligent backend system built to streamline the recruitment process. It accepts a job description (JD) and multiple candidate resumes, analyzes them using Natural Language Processing (NLP), ranks the resumes based on their relevance to the JD, and automatically schedules interviews for the top candidates.

⚙️ Features

📁 Resume Upload – Upload multiple resumes in supported formats (PDF/DOCX).

🧾 Job Description Input – Provide a detailed JD for the role.

🧠 NLP-based Resume Matching – Uses NLP techniques to extract, clean, and compare textual content between resumes and the JD.

📊 Candidate Ranking – Scores and ranks candidates based on similarity to the JD.

🗓️ Interview Scheduling – Automatically schedules interviews for shortlisted candidates.

💡 Planned Improvements:

Implement a rule-based or LLM-based system to flag candidates with partial matches but relevant skills.

Add a frontend dashboard for recruiters to visualize scores and schedules.

🧩 Tech Stack

Backend: Python, FastAPI

Database: MongoDB

Core Concepts: Natural Language Processing (NLP), Text Similarity, Ranking Algorithms

Libraries Used:

fastapi – REST API framework

pydantic – Data validation

pymongo – MongoDB integration

nltk, scikit-learn, spacy – Text preprocessing and similarity computation

🚀 How It Works

Upload Resumes & JD – User provides candidate resumes and the JD.

Text Extraction & Cleaning – NLP pipeline processes and tokenizes the content.

Similarity Computation – Uses TF-IDF vectorization and cosine similarity to evaluate match scores.

Ranking & Storage – Candidates are ranked based on scores and stored in MongoDB.

Interview Scheduling – Top candidates are automatically scheduled for interviews.
