import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Income AI Predictor",
    page_icon="💰",
    layout="wide"
)

# ---------------- CUSTOM CSS (dark hero theme) ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #05070d;
    background-image:
        linear-gradient(rgba(99,102,241,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.05) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* ---------- HERO ---------- */
.eyebrow {
    text-align: center;
    letter-spacing: 3px;
    font-size: 13px;
    font-weight: 700;
    color: #818cf8;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.hero-title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1.15;
    margin-bottom: 14px;
}

.hero-title .accent {
    color: #818cf8;
}

.hero-sub {
    text-align: center;
    font-size: 17px;
    color: #94a3b8;
    margin-bottom: 40px;
}

/* ---------- SECTION CARD ---------- */
.section-card {
    background-color: #0d1117;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 26px 28px;
    margin-bottom: 22px;
}

.section-heading {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 18px;
}

/* ---------- RESULT ---------- */
.result-box {
    padding: 24px;
    border-radius: 14px;
    text-align: center;
    font-size: 26px;
    font-weight: 800;
    border: 1px solid transparent;
    margin-bottom: 10px;
}

.success {
    background-color: rgba(74, 222, 128, 0.08);
    color: #4ade80;
    border-color: rgba(74, 222, 128, 0.3);
}

.low {
    background-color: rgba(248, 113, 113, 0.08);
    color: #f87171;
    border-color: rgba(248, 113, 113, 0.3);
}

/* ---------- FOOTER ---------- */
.footer {
    text-align: center;
    font-size: 12px;
    letter-spacing: 1px;
    color: #475569;
    margin-top: 50px;
    text-transform: uppercase;
}

.footer b {
    color: #94a3b8;
}

/* ---------- Streamlit widget overrides ---------- */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #818cf8);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 14px 0;
    font-size: 16px;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO HEADER ----------------
st.markdown("<div class='eyebrow'>Machine Learning · Income Prediction</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-title'>Income <span class='accent'>AI</span> Predictor</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<div class='hero-sub'>Enter a profile — the model estimates whether income is above or below $50K</div>",
    unsafe_allow_html=True
)

# ---------------- EDUCATION MAPPING ----------------
# educational-num in the classic Adult/Census dataset is a NUMBER,
# not a string. Map the dropdown label to the numeric code your
# model was trained on. Adjust these values to match your training data.
EDUCATION_MAP = {
    "HS-grad": 9,
    "Bachelors": 13,
    "Masters": 14,
    "Doctorate": 16
}

# ---------------- PERSONAL + WORK INFO ----------------
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-heading'>👤 Personal & Work Info</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 90, 30)
    workclass = st.selectbox("Workclass", ["Private", "Self-emp", "Gov", "Other"])
    education = st.selectbox("Education", list(EDUCATION_MAP.keys()))
    marital_status = st.selectbox("Marital Status", ["Married", "Single", "Divorced"])
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

with col2:
    occupation = st.text_input("Occupation", "Tech")
    relationship = st.text_input("Relationship", "Husband")
    race = st.selectbox("Race", ["White", "Black", "Asian", "Other"])
    native_country = st.text_input("Country", "United-States")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FINANCIAL INFO ----------------
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-heading'>📊 Financial Info</div>", unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)

with col3:
    capital_gain = st.number_input("Capital Gain", 0)

with col4:
    capital_loss = st.number_input("Capital Loss", 0)

with col5:
    hours_per_week = st.slider("Hours/Week", 1, 100, 40)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PREDICT BUTTON ----------------
btn = st.button("🚀  Predict Income", use_container_width=True)

if btn:

    url = "http://127.0.0.1:8000/predict"

    data = {
        "age": age,
        "workclass": workclass,
        "educational-num": EDUCATION_MAP[education],
        "marital-status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "gender": gender,
        "capital-gain": capital_gain,
        "capital-loss": capital_loss,
        "hours-per-week": hours_per_week,
        "native-country": native_country
    }

    try:
        res = requests.post(url, json=data, timeout=10)

        if res.status_code == 200:
            body = res.json()

            # Backend returns {"error": ...} on internal failure (e.g. unseen
            # category, column mismatch) instead of raising an HTTP error
            if "error" in body:
                st.error(f"Model Error: {body['error']}")
            else:
                result = body["prediction"]
                confidence = body.get("confidence")

                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-heading'>🎯 Prediction Result</div>", unsafe_allow_html=True)

                if result == ">50K":
                    st.markdown(f"<div class='result-box success'>💰 {result}</div>", unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown(f"<div class='result-box low'>📉 {result}</div>", unsafe_allow_html=True)

                if confidence is not None:
                    st.caption(f"Model confidence: {confidence * 100:.1f}%")
                else:
                    st.caption("Model analyzed demographic + financial features to predict income class.")

                st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.error(f"API Error {res.status_code}: {res.text}")

    except requests.exceptions.Timeout:
        st.error("Request timed out. Is the backend server running?")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure the FastAPI server is running on port 8000.")
    except Exception as e:
        st.error(f"Connection Error: {e}")

# ---------------- FOOTER ----------------
st.markdown(
    "<div class='footer'>Built with <b>Scikit-learn</b> · <b>FastAPI</b> · <b>Streamlit</b></div>",
    unsafe_allow_html=True
)