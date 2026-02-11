from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

# MongoDB Atlas connection
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.admin.command('ping')
    db = client[DB_NAME]
    print(f"✓ Connected to MongoDB Atlas: {DB_NAME}")
except Exception as e:
    print(f"✗ MongoDB Connection Error: {e}")
    raise
