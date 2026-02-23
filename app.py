import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Sri Lanka Internet Access Predictor", layout="wide")

st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #eef2f5;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    h1 {
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        color: #1a1f2e !important;
        text-align: center !important;
        margin-bottom: 0.3rem !important;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    .section-card {
        background: white;
        border-radius: 14px;
        padding: 15px 22px;
        margin-bottom: 18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 700;
        font-size: 1rem;
        color: #1a1f2e;
    }

    .stSelectbox label, .stSlider label, .stCheckbox label {
        font-size: 0.85rem !important;
        color: #374151 !important;
        font-weight: 500 !important;
        margin-bottom: 4px !important;
    }

    .stSelectbox > div > div {
        background: #f3f6f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        color: #1a1f2e !important;
        padding: 2px 8px !important;
    }

    .stSlider > div > div > div > div {
        background: #ef4444 !important;
    }

    .stSlider > div > div > div > div > div {
        background: #ef4444 !important;
        border: 2px solid #ef4444 !important;
    }

    .stSlider > div > div > div > div > div > div {
        color: #ef4444 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }

    .stCheckbox > label > div[data-testid="stCheckbox"] {
        border-color: #d1d5db !important;
        border-radius: 4px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2dd4bf, #00b8ad) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 14px 36px !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: opacity 0.2s !important;
        box-shadow: 0 4px 14px rgba(0, 212, 200, 0.35) !important;
    }

    .stButton > button:hover {
        opacity: 0.9 !important;
    }

    [data-testid="stAlert"] {
        margin-top: 20px !important;
        padding: 26px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        text-align: center;
    }

    [data-testid="column"] {
        padding: 0 10px !important;
    }

    hr { display: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Sri Lanka Internet Access Predictor</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Quickly predict household connectivity based on key demographic factors</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="section-card">📍 Location</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="section-card">👤 Representative</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="section-card">💼 Status & Assets</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    category_raw = st.selectbox("Living Area", ["Urban", "Rural"])
    district_raw = st.selectbox("District", ["Colombo", "Kandy", "Galle", "Jaffna"])

with col2:
    sex_raw = st.selectbox("Gender", ["Male", "Female"])
    age = st.slider("Representative's Age", 15, 80, 30)

with col3:
    education_raw = st.selectbox("Education Level", ["Primary", "O/L", "A/L", "Degree"])
    employment_raw = st.selectbox("Employment Status", ["Unemployed", "Student", "Employed"])

st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)
col_check1, col_check2, col_btn = st.columns(3)

with col_check1:
    smartphone_check = st.checkbox("Smartphone Available?", value=True)

with col_check2:
    laptop_check = st.checkbox("Laptop Available?", value=False)

with col_btn:
    predict_clicked = st.button("Predict Connectivity")

# Encoding (must match training)
category = 1 if category_raw == "Urban" else 0
sex = 1 if sex_raw == "Female" else 0
smartphone = 1 if smartphone_check else 0
laptop = 1 if laptop_check else 0

education_map = {"Primary": 0, "O/L": 1, "A/L": 2, "Degree": 3}
employment_map = {"Unemployed": 0, "Student": 1, "Employed": 2}
district_map = {"Colombo": 0, "Kandy": 1, "Galle": 2, "Jaffna": 3}

education = education_map[education_raw]
employment = employment_map[employment_raw]
district = district_map[district_raw]

# Create dataframe EXACTLY matching training
input_data = pd.DataFrame([[
    category,
    district,
    sex,
    age,
    education,
    employment,
    smartphone,
    laptop
]], columns=[
    "Category",
    "District",
    "4. Sex",
    "5. Age(as at last birthday)",
    "9. Level of education",
    "10. Employment status",
    "Smart phones_Home",
    "Laptop_Home"
])

if predict_clicked:
    model = joblib.load("internet_model.pkl")
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.success(f"✅  Likely to have Internet Access (Chance of having internet: {probability:.0%})")
    else:
        st.error(f"❌  Likely NOT to have Internet Access (Chance of having internet: {probability:.0%})")