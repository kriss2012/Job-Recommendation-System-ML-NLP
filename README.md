# 🧠 AI-Powered Job Recommendation System

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/kriss2012/Job-Recommendation-System-ML-NLP)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fkriss2012%2FJob-Recommendation-System-ML-NLP&root-directory=Frontend)

This project is an intelligent job recommendation web application that matches a user’s uploaded resume with relevant job listings using NLP techniques and cosine similarity. 

### 🌐 Split-Architecture Deployment

To optimize reliability and cost, this repository is structured to support a completely split deployment:
1. **Frontend (Vercel)**: A lightning-fast, high-performance static HTML/CSS/JS client located in the `/Frontend` folder.
2. **Backend API (Render)**: A python Flask API located in the `/Backend` folder, configured with CORS to allow secure request handling.

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

## 🌐 Deployment & Configuration Guide

To deploy this project seamlessly:

### 1. Backend on Render
- Simply click the **Deploy to Render** button at the top of this file.
- Under **Environment Variables**, you can set `MONGO_URI` if you want to use a custom MongoDB Atlas instance. Otherwise, it will automatically connect to a shared Atlas cluster out-of-the-box.
- Once deployed, copy your Render Web Service URL (e.g., `https://job-rec-backend.onrender.com`).
- **Seed the Database**: Hit the `/seed` path on your deployed Render service (e.g. `https://job-rec-backend.onrender.com/seed`) to automatically load the initial 12 job offers into MongoDB.

### 2. Frontend on Vercel
- Click the **Deploy with Vercel** button at the top.
- Vercel will clone the repo and automatically configure the `/Frontend` directory as the root folder.
- When the site opens:
  - Click the **Gear icon** in the bottom-right corner of the Login page.
  - Paste your Render Backend URL in the input field.
  - The connection badge will instantly verify health.
  - Click **Save Settings** – this URL is stored securely in your browser's local storage and used for all requests!


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
