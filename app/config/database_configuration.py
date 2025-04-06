from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
    # Kết nối MongoDB Atlas
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["university_db"]
    return db

