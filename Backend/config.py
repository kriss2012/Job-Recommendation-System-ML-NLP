import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://echorepairs45_db_user:Lddq4RVpKlZOb5Ws@cluster0.lhd9g1g.mongodb.net/?appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "jobrecdb")
