# Translated and unified version of all core logic for the AI-powered Job Recommendation System

from flask import Flask, request, render_template, redirect, url_for, jsonify
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import re
import bcrypt
import os
import matplotlib.pyplot as plt
import spacy

from BD.Connexion import db, client
from Models.skills import skills
from Models.User import User
from Models.OffreEmploi import OffreEmploi
from Models.similarityOffre import SimilarityOffre
from Models.offres_emploi_test import OffreEmploiTest
from Models.offres_emploi_train import OffreEmploiTrain

nlp = spacy.load("en_core_web_sm")


# Load Spacy model with error handling
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# TF-IDF Vectorizer setup
custom_stopwords = [
    "the", "and", "of", "for", "with", "in", "on", "at", "by", "an",
    "a", "is", "to", "from", "as", "are", "it", "this", "that"
]
tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words=custom_stopwords)

app = Flask(__name__, template_folder='../templates')
app.config['STATIC_FOLDER'] = 'static'
user_collection = db['user']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = user_collection.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return redirect('index_cv')
        else:
            error_message = "Incorrect email or password"
    return render_template('index.html', error_message=error_message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_message = None
    if request.method == 'POST':
        first_name = request.form.get('prenom')
        last_name = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = user_collection.find_one({'email': email})
        if existing_user:
            error_message = "Email already exists"
        else:
            new_user = User(last_name, first_name, email, password)
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_collection.insert_one({
                'nom': new_user.nom,
                'prenom': new_user.prenom,
                'email': new_user.email,
                'password': hashed_password
            })
            return redirect(url_for('index_cv'))
    return render_template('index_inscrire.html', error_message=error_message)

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/index_cv')
def index_cv():
    return render_template('index_cv.html')

def clean_and_preprocess(text):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    text = re.sub(r'\d{10,}', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    words = text.split()
    filtered_words = [word for word in words if word not in custom_stopwords]
    return ' '.join(filtered_words)

@app.route('/process_uploaded_cv', methods=['POST'])
def process_uploaded_cv():
    if 'pdfFile' not in request.files or request.files['pdfFile'].filename == '':
        return "No valid resume file uploaded."

    uploaded_cv = request.files['pdfFile']
    pdf_reader = PdfReader(uploaded_cv)
    cv_text = "".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    cleaned_cv = clean_and_preprocess(cv_text)
    tfidf_vectorizer.fit(skills)
    tfidf_vector_for_user_cv = tfidf_vectorizer.transform([cleaned_cv])

    offers_collection = db["offres_emploi"]
    cursor = offers_collection.find({})

    similarities = []
    offer_names = []
    data = []

    for doc in cursor:
        name = doc['name']
        combined_text = doc['combined_text']
        link = doc['lien']
        job_offer = OffreEmploi(name, combined_text, link)

        cleaned_offer_text = clean_and_preprocess(job_offer.combined_text)
        tfidf_vector_for_offer = tfidf_vectorizer.transform([cleaned_offer_text])
        similarity_score = cosine_similarity(tfidf_vector_for_user_cv, tfidf_vector_for_offer)

        if similarity_score is not None:
            similarity_score = similarity_score[0][0]
            similarity_entry = SimilarityOffre(link, similarity_score)
            data.append(similarity_entry)
            similarities.append(similarity_score)
            offer_names.append(name)

    filtered_recommendations = [
        {'lienOffre': job.lien, 'similarity': job.similarity}
        for job in data if job.similarity > 0.2
    ]
    filtered_recommendations.sort(key=lambda x: x['similarity'], reverse=True)

    plt.figure(figsize=(10, 6))
    plt.bar(offer_names, similarities, color='blue')
    plt.axhline(y=0.9, color='red', linestyle='--', label='CV Similarity Threshold')
    plt.title("Similarity between user's resume and job offers")
    plt.xlabel('Job Offer')
    plt.ylabel('Similarity Score')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig('static/similarite.png')
    plt.close()

    return render_template('offre.html', similarity_image='similarite.png', recommendations=filtered_recommendations)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    

