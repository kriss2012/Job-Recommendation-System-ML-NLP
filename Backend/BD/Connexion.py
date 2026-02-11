from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
# Atlas connection configuration
MONGO_URI_ATLAS = "mongodb+srv://echorepairs45_db_user:Lddq4RVpKlZOb5Ws@cluster0.lhd9g1g.mongodb.net/?appName=Cluster0"
client_atlas = MongoClient(MONGO_URI_ATLAS)
db_atlas = client_atlas[DB_NAME]
