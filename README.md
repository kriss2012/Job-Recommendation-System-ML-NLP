# 🧠 AI-Powered Job Recommendation System

This project is an intelligent job recommendation web application that matches a user’s uploaded resume with relevant job listings using NLP techniques and cosine similarity. It uses TF-IDF to extract features from job descriptions and the user’s CV and compares them to recommend the most relevant positions.

---

## 🚀 Features

- Upload your resume as a PDF
- Automatic resume parsing with text cleaning
- Skill matching using TF-IDF and cosine similarity
- Job listings stored in MongoDB
- Secure user authentication (login/signup with hashed passwords)
- Visual chart showing similarity scores
- RESTful Flask backend
- Modular structure with Docker-ready setup

---

## 📂 Project Structure

Job-Recommendation-System/
├── app.py                       # Main Flask application
├── config.py                    # Loads environment variables
├── requirements.txt             # Python dependencies
├── .env                         # MongoDB credentials
├── BD/
│   └── Connexion.py             # MongoDB connection setup
├── Models/
│   ├── User.py                  # User model
│   ├── OffreEmploi.py           # Job posting model
│   └── similarityOffre.py       # Recommendation wrapper
├── processing.py                # TF-IDF vectorizer & preprocessing
├── templates/
│   ├── layout.html
│   ├── index.html               # Login
│   ├── index_inscrire.html      # Signup
│   ├── index_cv.html            # CV upload page
│   └── offre.html               # Recommendation results
├── static/
│   ├── images/
│   └── css/, js/                # Styling & JS
├── data/
│   └── jobs.json                # Job descriptions dataset
└── README.md

## 🛠️ Installation

### 📌 Prerequisites

- Python 3.8+
- pip
- MongoDB (local or MongoDB Atlas)
- virtualenv (recommended)

---

### 📥 Clone the Repository

git clone https://github.com/your-username/job-recommendation-system.git
cd job-recommendation-system


---

### 📦 Set Up Environment

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


---

### 📄 Install Dependencies

pip install -r requirements.txt
python -m spacy download fr_core_news_sm


---

### ⚙️ Configure MongoDB

Create a `.env` file in the project root:


MONGO_URI=mongodb://localhost:27017/
DB_NAME=jobrecdb


> For MongoDB Atlas, replace with your connection string.

---

### 🧠 Add Job Data

Load `data/jobs.json` into MongoDB:


mongoimport --db jobrecdb --collection offres_emploi --file data/jobs.json --jsonArray

---

## ▶️ Run the Application

python app.py

Visit: [http://localhost:5002](http://localhost:5002)

---

## 🔐 Authentication

* **Sign Up**: `/signup`
* **Login**: `/login`
* Passwords are securely hashed with `bcrypt`.

---

## 📊 Recommendations

* Upload a PDF resume
* System calculates cosine similarity with job descriptions
* Visual chart displayed with top matches
* Thresholds can be adjusted in `app.py`

---

## 🐳 Docker (Optional)

### 🧱 Build the Image


docker build -t job-recommendation-system .


### ▶️ Run the Container


docker run -p 5002:5002 --env-file .env job-recommendation-system

---

## 🌐 Deployment

You can deploy the app using:

* Render / Railway / Heroku (Docker-based)
* MongoDB Atlas for production DB

---

## 🔐 Security Notes

* Do **not** commit `.env` or credentials.
* Uploaded resumes are processed in-memory and never saved.
* Input forms are validated and sanitized.
* Mongo queries are safe with parameterized lookups.

---

## 📚 Tech Stack

* **Python / Flask**
* **MongoDB**
* **Jinja2 Templates**
* **NLP with spaCy & scikit-learn**
* **TF-IDF & Cosine Similarity**
* **bcrypt** for password hashing

## 📸 Screenshot

![Similarity Chart Example](static/similarite.png)

## 📝 License

MIT License. © 2026 Krishna Patil
