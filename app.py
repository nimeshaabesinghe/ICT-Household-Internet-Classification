import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("internet_model.pkl")

st.title("Sri Lanka Internet Access Prediction")

st.write("Enter household details below:")

# User Inputs
category = st.selectbox("Category", ["Urban", "Rural"])
district = st.selectbox("District", ["Colombo", "Kandy", "Galle", "Jaffna"])
sex = st.selectbox("Sex", ["Male", "Female"])
age = st.slider("Age", 15, 80, 30)
education = st.selectbox("Education Level", ["Primary", "O/L", "A/L", "Degree"])
employment = st.selectbox("Employment Status", ["Unemployed", "Student", "Employed"])
smartphone = st.selectbox("Smartphone at Home", ["Yes", "No"])
laptop = st.selectbox("Laptop at Home", ["Yes", "No"])

# Encoding (must match training)
category = 1 if category == "Urban" else 0
sex = 1 if sex == "Female" else 0
smartphone = 1 if smartphone == "Yes" else 0
laptop = 1 if laptop == "Yes" else 0

education_map = {"Primary":0, "O/L":1, "A/L":2, "Degree":3}
employment_map = {"Unemployed":0, "Student":1, "Employed":2}
district_map = {"Colombo":0, "Kandy":1, "Galle":2, "Jaffna":3}

education = education_map[education]
employment = employment_map[employment]
district = district_map[district]

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

if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.success(f"Likely to have Internet Access (Probability: {probability:.2f})")
    else:
        st.error(f"Likely NOT to have Internet Access (Probability: {probability:.2f})")