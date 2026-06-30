# Seed Script for CareerMatch AI
# Populates the 'offres_emploi' collection with realistic production-ready job listings.

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load configuration
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://echorepairs45_db_user:Lddq4RVpKlZOb5Ws@cluster0.lhd9g1g.mongodb.net/?appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "jobrecdb")

def seed():
    print(f"Connecting to MongoDB: {DB_NAME}...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["offres_emploi"]
    
    # Clear existing offers
    print("Clearing existing job offers...")
    collection.delete_many({})
    
    # 12 Realistic job listings with varying skills for matching
    job_listings = [
        {
            "name": "Senior Machine Learning Engineer (NLP)",
            "company": "DeepMind Technologies",
            "location": "London, UK (Hybrid)",
            "job_type": "Full-time",
            "salary": "£95,000 - £120,000",
            "lien": "https://careers.google.com/jobs/results/deepmind-ml-nlp",
            "description": "We are seeking a Senior ML Engineer specializing in Natural Language Processing (NLP). You will design and deploy large language models, refine text processing pipelines, and train models using scikit-learn, PyTorch, and SpaCy. Strong expertise in python, text processing, and TF-IDF similarity vectors is required.",
            "combined_text": "senior machine learning engineer nlp natural language processing python spacy pytorch tfidf tf-idf scikit-learn pandas numpy text processing vectorization machine learning model deployment engineering data science"
        },
        {
            "name": "AI & NLP Research Scientist",
            "company": "Cognitive AI Lab",
            "location": "Remote (US/Canada)",
            "job_type": "Remote",
            "salary": "$130,000 - $160,000",
            "lien": "https://example.com/jobs/cognitive-nlp-researcher",
            "description": "Join our research division to advance the state-of-the-art in text summarization and text classification. The ideal candidate has strong foundations in computational linguistics, python, NLP, spacy model training, scikit-learn classification, and vector embeddings.",
            "combined_text": "ai nlp research scientist computational linguistics python nlp spacy scikit-learn vector embeddings classification parsing tokenization nltk text processing"
        },
        {
            "name": "Python Developer (Data Science & ML)",
            "company": "Alpha Tech Solutions",
            "location": "Paris, France",
            "job_type": "Full-time",
            "salary": "€55,000 - €70,000",
            "lien": "https://example.com/jobs/alpha-python-ds",
            "description": "We are hiring a Python Software Engineer to join our analytics squad. You will build Flask microservices, clean unstructured resume text data, and extract skills using regular expressions, spacy, and scikit-learn models.",
            "combined_text": "python developer data science machine learning flask flask-apis spacy scikit-learn pandas numpy regex cleaning parsing data science engineering databases"
        },
        {
            "name": "NLP Engineer - Chatbots & Voice AI",
            "company": "SpeakEasy Corp",
            "location": "San Francisco, CA (Onsite)",
            "job_type": "Full-time",
            "salary": "$110,000 - $145,000",
            "lien": "https://example.com/jobs/speakeasy-nlp-chatbot",
            "description": "Build the next generation of conversational AI. Work with python, NLP libraries, NLTK, Spacy, and sklearn classifiers to build robust speech-to-text and intent-matching pipelines.",
            "combined_text": "nlp engineer chatbots voice ai conversational python nltk spacy sklearn classification speech to text intent mapping pipelines"
        },
        {
            "name": "Data Scientist - Personalization Systems",
            "company": "StreamFlix Inc.",
            "location": "Los Angeles, CA",
            "job_type": "Hybrid",
            "salary": "$140,000",
            "lien": "https://example.com/jobs/streamflix-data-scientist",
            "description": "Optimize our personalization engine. Leverage machine learning, pandas, numpy, scikit-learn, and cosine similarity matrices to match user profiles with dynamic content categories.",
            "combined_text": "data scientist personalization systems machine learning pandas numpy scikit-learn cosine similarity recommendation engine analysis math sql"
        },
        {
            "name": "Full-Stack Web Developer (Python & React)",
            "company": "LaunchPad Startups",
            "location": "Berlin, Germany",
            "job_type": "Contract",
            "salary": "€80 - €100 / hr",
            "lien": "https://example.com/jobs/berlin-full-stack",
            "description": "We need a contract developer to build an AI dashboard. Experience with Python (Flask/Django), HTML5, custom CSS (Neo-brutalist design preferred), and React frontend components. Some exposure to scikit-learn is a plus.",
            "combined_text": "full-stack web developer python react flask django html5 css javascript database postgresql frontend dashboard"
        },
        {
            "name": "Backend Engineer (Django / MongoDB)",
            "company": "Database Flow LLC",
            "location": "London, UK",
            "job_type": "Full-time",
            "salary": "£60,000 - £75,000",
            "lien": "https://example.com/jobs/dbflow-django-backend",
            "description": "Build high-throughput backend services using Django, Celery, and MongoDB. Help optimize search indexing, user signup workflows, and API responses.",
            "combined_text": "backend engineer django mongodb python celery sql nosql api integration search indexing databases redis"
        },
        {
            "name": "Machine Learning Intern",
            "company": "FutureAI Research",
            "location": "Boston, MA",
            "job_type": "Internship",
            "salary": "$4,000 / month",
            "lien": "https://example.com/jobs/futureai-ml-intern",
            "description": "We are seeking a graduate student for an ML internship. Work on data cleansing, training scikit-learn classification models, parsing documents, and evaluating cosine similarities of text sets.",
            "combined_text": "machine learning intern data cleansing training scikit-learn classification parsing pdf documents cosine similarity research python pandas"
        },
        {
            "name": "UI/UX Designer (Brutalist Web Design)",
            "company": "NeoCulture Studio",
            "location": "Amsterdam, Netherlands",
            "job_type": "Part-time",
            "salary": "€30,000",
            "lien": "https://example.com/jobs/neoculture-uiux-designer",
            "description": "Looking for a designer obsessed with Neo-Brutalist layouts, high-contrast borders, solid shadows, and bold typography. Design mobile-responsive web apps and design systems.",
            "combined_text": "ui ux designer brutalist web design high contrast solid shadows bold typography wireframes figma css design systems html"
        },
        {
            "name": "DevOps Engineer (AWS & Docker)",
            "company": "CloudGrid Systems",
            "location": "Seattle, WA",
            "job_type": "Full-time",
            "salary": "$125,000 - $150,000",
            "lien": "https://example.com/jobs/cloudgrid-devops",
            "description": "Maintain our cloud infrastructure. Automate deployments using Docker, Kubernetes, AWS CloudFormation, and Jenkins pipelines. Monitor server health and database replicas.",
            "combined_text": "devops engineer aws docker kubernetes cloudformation jenkins CI CD automation sysadmin linux scripting"
        },
        {
            "name": "Junior Frontend Engineer (React)",
            "company": "FinTech Innovations",
            "location": "New York, NY",
            "job_type": "Full-time",
            "salary": "$85,000",
            "lien": "https://example.com/jobs/fintech-frontend-jr",
            "description": "Help craft beautiful dashboard components. Proficient in React, JavaScript, CSS flexbox/grid, and standard responsive layout configurations.",
            "combined_text": "junior frontend engineer react javascript css css-grid html web apps dashboard git typescript components"
        },
        {
            "name": "Database Administrator (MongoDB & PostgreSQL)",
            "company": "DataSafe Solutions",
            "location": "Toronto, Canada",
            "job_type": "Full-time",
            "salary": "$90,000 - $110,000",
            "lien": "https://example.com/jobs/datasafe-dba",
            "description": "Manage security, backup, replica sets, and query optimization for MongoDB Atlas and Postgres databases. Implement security policies and user access controls.",
            "combined_text": "database administrator dba mongodb postgresql replica sets backups query optimization security admin access controls"
        }
    ]
    
    collection.insert_many(job_listings)
    print(f"Successfully seeded {len(job_listings)} job offers into database!")
    client.close()

if __name__ == "__main__":
    seed()
