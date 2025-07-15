# 🤖 Passive CAPTCHA Detection System

A smart and seamless way to differentiate bots from human users — **without interrupting the user experience**.  
This project was built during **HackAttack 2025** at *Sreyas Institute of Engineering and Technology* by team **Vitality**.

## 🔍 What It Does

Traditional CAPTCHA systems often hurt user experience and accessibility.  
This system uses **passive behavioral and environmental data** (like mouse movements, scroll behavior, device specs) to detect bots in the background — powered by a trained **machine learning model**.

## 🌟 Key Features

- ✅ No user input required — 100% passive detection
- 📈 Machine Learning based human vs bot classification
- 🔍 Tracks mouse, scroll, clicks, keystrokes, dwell time
- 🔐 Secured with API key validation
- 📊 Real-time session logging and dashboard for admins
- 🔁 Supports retraining on real user data

## 🧰 Tech Stack

| Layer     | Tech Used                          |
|-----------|------------------------------------|
| Frontend  | HTML, CSS, JavaScript              |
| SDK       | Vanilla JS (`passive-tracker.js`)  |
| Backend   | Python, FastAPI, Uvicorn           |
| ML Model  | Scikit-learn (RandomForest)        |
| Storage   | JSONL log file (sessions)          |
| Dashboard | HTML + Chart.js                    |

## 📁 Project Structure

```
passive-captcha/
├── frontend/            # Static site with tracking SDK
│   ├── index.html
│   └── passive-tracker.js
│
├── backend-api/         # FastAPI backend
│   ├── main.py          # API + CORS + validation
│   ├── utils.py         # Feature extraction
│   ├── requirements.txt
│   ├── bot_detector_bundle.joblib
│   ├── raw_data/
│   └── sessions.jsonl
│
├── ml_model/            # Training / retraining scripts
│   ├── train_from_csv.py
│   └── retrain_model.py
│
├── dashboard/
│   └── dashboard.html
```

## 🚀 How to Run It Locally

### 🖥 Backend (API Server)

```bash
cd backend-api
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```
Visit Swagger UI at: `http://localhost:5000/docs`

### 🌐 Frontend

You can open `frontend/index.html` with Live Server or any static server:
```bash
cd frontend
npx serve .
```
Or just open `index.html` directly in your browser.

### 📦 Model Training (Optional)

To train a new model on your CSV:
```bash
python ml_model/train_from_csv.py
```

To retrain using live session logs:
```bash
python ml_model/retrain_model.py
```

The trained model output will be:  
`backend-api/bot_detector_bundle.joblib`

### 🔐 API Key Protection

The API is secured using an `x-api-key` header.

Update **main.py**:
```python
API_KEY = "your-secure-key"
```
Update **passive-tracker.js**:
```js
headers: {
  "x-api-key": "your-secure-key"
}
```

### 📊 Dashboard

View logged sessions and analytics:  
Open `dashboard/dashboard.html` in your browser.

## 📌 Deployment Recommendations

| Component | Recommended Hosting               |
|-----------|----------------------------------|
| Frontend  | GitHub Pages / Netlify           |
| Backend   | Render / Railway (FastAPI)       |

Update fetch URL in `passive-tracker.js` to point to your deployed backend:
```js
fetch("https://your-api.onrender.com/api/verify", { ... });
```

## 🙌 Team Credits

- 👥 Built by Team Vitality during HackAttack 2025
- 🏫 Hosted by Sreyas Institute of Engineering and Technology
- 🎉 Special thanks to Shylee Preetham and the organizing team

