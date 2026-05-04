# 🏙️ Mumbai House Price Predictor

A **Streamlit web application** that predicts residential property prices in Mumbai using a trained **Decision Tree Regressor** model (97.9% accuracy).

[![CI – Test Streamlit App](https://github.com/Manavdarji2/PricePrediction/actions/workflows/ci.yml/badge.svg)](https://github.com/Manavdarji2/PricePrediction/actions/workflows/ci.yml)

---

## 🚀 Live App

Deploy this app instantly on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Fork / push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set **Main file path** to `app.py`
4. Click **Deploy**

---

## 📦 Project Structure

```
PricePrediction/
├── app.py                          # Streamlit frontend
├── requirements.txt                # Python dependencies
├── Mumbai-price-pridection.pickle  # Trained ML model
├── house_price_mumbai.csv          # Raw dataset
├── Price-Pridection.ipynb          # Model training notebook
└── .github/
    └── workflows/
        └── ci.yml                  # GitHub Actions CI pipeline
```

---

## 🛠️ Running Locally

```bash
# 1. Clone the repository
git clone https://github.com/Manavdarji2/PricePrediction.git
cd PricePrediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

The app will open at **http://localhost:8501**.

---

## 🧠 Model Details

| Property | Value |
|---|---|
| Algorithm | Decision Tree Regressor |
| Accuracy (test set) | **97.9%** |
| Cross-val accuracy | ~88% (ShuffleSplit, 8 folds) |
| Training samples | 3,356 |
| Features | Total sqft, Price/sqft, BHK, Location (one-hot) |
| Target | Price in Crore (₹) |

### Input Features

| Feature | Type | Description |
|---|---|---|
| Location | Categorical | Mumbai suburb (20+ areas) |
| BHK | Integer 1–5 | Number of bedrooms |
| Total Area | Integer (sq ft) | Carpet / built-up area |
| Price per sq ft | Integer (₹) | Local market rate |

---

## ⚙️ CI/CD Pipeline

The `.github/workflows/ci.yml` workflow runs on every push/PR to `main`:

1. **Install dependencies** from `requirements.txt`
2. **Verify all imports** resolve correctly
3. **Check the model file** is present
4. **Smoke-test** the prediction logic end-to-end

---

## 📊 Data Preprocessing (Notebook)

1. Convert price strings (`Cr` / `L`) → float in Crore
2. Remove East/West suffixes from location names
3. Drop locations with fewer than 25 listings
4. Filter BHK types to standard 1–5 BHK Apartments
5. Remove outliers using BHK price-per-sqft statistics
6. One-hot encode Location (drop first to avoid multicollinearity)
7. Train/test split (80/20), GridSearchCV for hyperparameter tuning

---

## 📝 License

MIT
