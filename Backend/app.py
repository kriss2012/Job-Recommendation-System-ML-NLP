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

# Load Spacy model with error handling
try:
    nlp = spacy.load("en_core_web_sm")
    print("[OK] Spacy model loaded successfully")
except OSError:
    print("[INFO] Downloading Spacy model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    print("[OK] Spacy model installed and loaded")

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
            return redirect(url_for('index_cv'))
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
        name = doc.get('name', 'Job Offer')
        combined_text = doc.get('combined_text', '')
        link = doc.get('lien', '#')
        description = doc.get('description', combined_text[:200] + '...' if len(combined_text) > 200 else combined_text)
        location = doc.get('location', 'Not specified')
        job_type = doc.get('job_type', 'Not specified')
        salary = doc.get('salary', 'Not specified')
        company = doc.get('company', 'Not specified')
        
        job_offer = OffreEmploi(name, combined_text, link)

        cleaned_offer_text = clean_and_preprocess(job_offer.combined_text)
        tfidf_vector_for_offer = tfidf_vectorizer.transform([cleaned_offer_text])
        similarity_score = cosine_similarity(tfidf_vector_for_user_cv, tfidf_vector_for_offer)

        if similarity_score is not None:
            similarity_score = similarity_score[0][0]
            data.append({
                'name': name,
                'link': link,
                'description': description,
                'location': location,
                'job_type': job_type,
                'salary': salary,
                'company': company,
                'similarity': similarity_score
            })
            similarities.append(similarity_score)
            offer_names.append(name)

    # Filter and sort recommendations
    filtered_recommendations = [job for job in data if job['similarity'] > 0.2]
    filtered_recommendations.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Get top 10 for chart
    top_jobs = filtered_recommendations[:10] if filtered_recommendations else data[:10]
    top_names = [job['name'] for job in top_jobs]
    top_scores = [job['similarity'] for job in top_jobs]

    # Create enhanced visualization (Neo-Brutalist Styled)
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='#ffffff')
    ax.set_facecolor('#ffffff')
    
    # Border & grid styling (brutalist heavy borders)
    for spine in ['bottom', 'left', 'top', 'right']:
        ax.spines[spine].set_color('#000000')
        ax.spines[spine].set_linewidth(3)
        
    ax.tick_params(colors='#000000', labelsize=10, width=3)
    
    # Set labels
    ax.set_xlabel('Similarity Score', fontsize=12, fontweight='bold', color='#000000', labelpad=10)
    ax.set_title("Resume Match Similarity Analysis", fontsize=14, fontweight='black', color='#000000', pad=15)
    ax.set_xlim(0, 1)
    
    # Create horizontal bars (Yellow bars with thick black border)
    bars = ax.barh(top_names, top_scores, color='#ffe600', edgecolor='#000000', linewidth=2.5, height=0.6)
    
    # Threshold lines
    ax.axvline(x=0.7, color='#4ade80', linestyle='--', linewidth=2.5, label='High Match Threshold (0.7)')
    ax.axvline(x=0.4, color='#facc15', linestyle='--', linewidth=2.5, label='Medium Match Threshold (0.4)')
    
    # Legend customization
    legend = ax.legend(loc='lower right', facecolor='#ffffff', edgecolor='#000000')
    legend.get_frame().set_linewidth(2.5)
    for text in legend.get_texts():
        text.set_color('#000000')
        text.set_fontweight('bold')
        text.set_fontsize(10)
        
    # Score labels on bars
    for bar, score in zip(bars, top_scores):
        ax.text(score + 0.02, bar.get_y() + bar.get_height()/2, f'{score:.1%}', 
                va='center', fontweight='bold', color='#000000', fontsize=10)
        
    plt.tight_layout()
    chart_path = os.path.join(os.path.dirname(__file__), 'static', 'similarite.png')
    plt.savefig(chart_path, dpi=100, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    stats = {
        'total_jobs': len(data),
        'matched_jobs': len(filtered_recommendations),
        'avg_similarity': sum(job['similarity'] for job in data) / len(data) if data else 0,
        'top_score': max([job['similarity'] for job in data]) if data else 0
    }

    return render_template('offre.html', 
                         similarity_image='similarite.png', 
                         recommendations=filtered_recommendations,
                         stats=stats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    print(f"\n* Starting Flask app on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
    

