from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["smart_scheduler"]  # ✅ Ensure this matches your actual DB name in MongoDB Atlas
resumes_collection = db["resumes"]    # ✅ Collection name you will use
