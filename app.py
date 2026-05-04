import streamlit as st
import pickle
import numpy as np
import math
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mumbai House Price Predictor",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ─── Background ─── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* ─── Main container ─── */
.main .block-container {
    padding: 2rem 1.5rem 4rem;
    max-width: 820px;
}

/* ─── Hero section ─── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-icon {
    font-size: 4rem;
    margin-bottom: .5rem;
    filter: drop-shadow(0 0 20px rgba(129,140,248,.6));
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #c084fc, #fb7185);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 .4rem;
    line-height: 1.2;
}
.hero p {
    color: rgba(255,255,255,.6);
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
}

/* ─── Divider ─── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(129,140,248,.4), transparent);
    margin: 1.8rem 0;
}

/* ─── Card ─── */
.card {
    background: rgba(255,255,255,.05);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,.3);
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: rgba(255,255,255,.9);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}

/* ─── Streamlit input overrides ─── */
label {
    color: rgba(255,255,255,.75) !important;
    font-size: .875rem !important;
    font-weight: 500 !important;
}
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,.08) !important;
    border: 1px solid rgba(255,255,255,.15) !important;
    border-radius: 10px !important;
    color: #fff !important;
}
.stSelectbox > div > div:hover,
.stNumberInput > div > div > input:focus {
    border-color: rgba(129,140,248,.6) !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,.15) !important;
}

/* ─── Button ─── */
.stButton > button {
    width: 100%;
    padding: .9rem 1.5rem;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: .5px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    color: #fff;
    cursor: pointer;
    transition: all .25s ease;
    box-shadow: 0 4px 20px rgba(129,140,248,.35);
    margin-top: .5rem;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(129,140,248,.5);
    background: linear-gradient(90deg, #6366f1, #a855f7);
}

/* ─── Result box ─── */
.result-box {
    background: linear-gradient(135deg, rgba(129,140,248,.15), rgba(192,132,252,.15));
    border: 1px solid rgba(129,140,248,.35);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    margin-top: 1.5rem;
    animation: fadeInUp .5s ease;
}
.result-label {
    color: rgba(255,255,255,.6);
    font-size: .9rem;
    font-weight: 500;
    margin-bottom: .6rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.result-price {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #c084fc, #fb7185);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: .4rem 0;
}
.result-sub {
    color: rgba(255,255,255,.45);
    font-size: .8rem;
}
.result-note {
    color: rgba(255,255,255,.5);
    font-size: .78rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,.1);
}

/* ─── Badge ─── */
.badge {
    display: inline-block;
    padding: .25rem .65rem;
    border-radius: 999px;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .4px;
    text-transform: uppercase;
}
.badge-purple { background: rgba(129,140,248,.2); color: #818cf8; border: 1px solid rgba(129,140,248,.3); }
.badge-green  { background: rgba(52,211,153,.2);  color: #34d399; border: 1px solid rgba(52,211,153,.3);  }

/* ─── Info tiles ─── */
.tiles { display: flex; gap: 1rem; margin-top: 1rem; }
.tile {
    flex: 1;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.tile-val { font-size: 1.5rem; font-weight: 700; color: #c084fc; }
.tile-lbl { font-size: .72rem; color: rgba(255,255,255,.5); margin-top: .2rem; text-transform: uppercase; letter-spacing: .8px; }

/* ─── Footer ─── */
.footer {
    text-align: center;
    color: rgba(255,255,255,.3);
    font-size: .75rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,.08);
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# tell it based onold data so price may be low or high
# and also mention that the model is trained on 2022 data
st.title("Real Estate Price Prediction")
st.markdown("<div class='footer'>This model is trained on 2022 data. The price may be low or high based on the old data.</div>", unsafe_allow_html=True)

# ── Load model & feature columns ───────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("Mumbai-price-pridection.pickle", "rb") as f:
        model = pickle.load(f)
    return model

# We can get FEATURE_COLS directly from the model, or use the exact list from the trained model:
FEATURE_COLS = [
    'Total sqft', 'price_sqft', 'bhk_no', 'Ambernath', 'Andheri', 'Badlapur',
    'Bandra', 'Bhandup', 'Bhayandar', 'Bhiwandi', 'Borivali', 'Byculla', 'Chembur',
    'Dahisar', 'Diva Gaon', 'Dombivali', 'Ghatkopar', 'Goregaon', 'Jogeshwari',
    'Kalwa', 'Kalyan', 'Kandivali', 'Karanjade', 'Karjat', 'Kharghar',
    'Koper Khairane', 'Kurla', 'Malad', 'Mira Road', 'Mulund', 'Naigaon', 'Neral',
    'Palghar', 'Panvel', 'Powai', 'Rasayani', 'Santacruz', 'Taloja', 'Thane', 'Ulwe',
    'Vasai', 'Virar'
]

LOCATIONS = sorted(FEATURE_COLS[3:])


def predict_price(model, location, price_sqft, bhk_no, total_sqft):
    data = np.zeros(len(FEATURE_COLS))
    data[0] = total_sqft
    data[1] = price_sqft
    data[2] = bhk_no
    
    if location in FEATURE_COLS:
        idx = FEATURE_COLS.index(location)
        data[idx] = 1
        
    df_input = pd.DataFrame([data], columns=FEATURE_COLS)
    price_cr = model.predict(df_input)[0]
    return price_cr


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-icon">🏙️</div>
  <h1>Mumbai House Price Predictor</h1>
  <p>AI-powered estimates for Mumbai's residential property market</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Model info ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="tile">
      <div class="tile-val">97.9%</div>
      <div class="tile-lbl">Model Accuracy</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="tile">
      <div class="tile-val">3,356</div>
      <div class="tile-lbl">Training Samples</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="tile">
      <div class="tile-val">20+</div>
      <div class="tile-lbl">Locations</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔍 Property Details</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    location = st.selectbox(
        "📍 Location",
        options=LOCATIONS,
        index=LOCATIONS.index("Andheri"),
        help="Select the Mumbai suburb / area",
    )
    bhk = st.selectbox(
        "🛏️ BHK Configuration",
        options=[1, 2, 3, 4, 5],
        index=1,
        format_func=lambda x: f"{x} BHK Apartment",
    )

with col_b:
    total_sqft = st.number_input(
        "📐 Total Area (sq ft)",
        min_value=100,
        max_value=20_000,
        value=750,
        step=50,
        help="Carpet / built-up area in square feet",
    )
    price_per_sqft = st.number_input(
        "💰 Price per sq ft (₹)",
        min_value=100,
        max_value=1_50_000,
        value=12_000,
        step=500,
        help="Current market rate per square foot in the area",
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── Predict button ─────────────────────────────────────────────────────────────
predict_clicked = st.button("✨ Predict Price", use_container_width=True)

# ── Result ─────────────────────────────────────────────────────────────────────
if predict_clicked:
    try:
        model = load_model()
        price_cr = predict_price(model, location, price_per_sqft, bhk, total_sqft)
        price_cr = max(price_cr, 0)  # guard against negative predictions

        price_inr = math.ceil(price_cr * 1_00_00_000)

        if price_cr >= 1:
            display_price = f"₹ {price_cr:.2f} Cr"
            sub = f"≈ ₹ {price_inr:,}"
        else:
            price_lakh = price_cr * 100
            display_price = f"₹ {price_lakh:.2f} L"
            sub = f"≈ ₹ {price_inr:,}"

        st.markdown(f"""
        <div class="result-box">
          <div class="result-label">Estimated Market Price</div>
          <div class="result-price">{display_price}</div>
          <div class="result-sub">{sub}</div>
          <div class="result-note">
            Estimate based on {bhk} BHK · {total_sqft:,} sq ft · {location}<br>
            @ ₹{price_per_sqft:,}/sq ft &nbsp;|&nbsp; Model accuracy: 97.9%
          </div>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("❌ Model file not found. Make sure `Mumbai-price-pridection.pickle` is in the project root.")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Built with Streamlit · DecisionTreeRegressor · Mumbai Housing Dataset<br>
  Predictions are estimates only — consult a real estate professional for accurate valuations.
</div>
""", unsafe_allow_html=True)
