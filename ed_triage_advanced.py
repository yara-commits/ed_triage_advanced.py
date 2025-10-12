import streamlit as st
from gtts import gTTS
import base64
import os

# --- Inputs with keys ---
symptom = st.text_input("Enter your symptoms:", key="symptom_input")
age = st.number_input("Your age:", min_value=0, max_value=120, key="age_input")

# --- Reset button ---
if st.button("Reset"):
    st.session_state["symptom_input"] = ""
    st.session_state["age_input"] = 0
    st.experimental_rerun()

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="ED Triage Assistant", page_icon="🏥", layout="centered")

# ---------- WELCOME MESSAGE ----------
welcome_text = "Welcome to our ED triage system. Please be calm. Everything will be fine Our system is here to help assess your symptoms quickly and safely.."

## ---------- CREATE / SAVE AUDIO FILE ----------
audio_path = "welcome.mp3"
if not os.path.exists(audio_path):
    from gtts import gTTS
    tts = gTTS("Welcome to our ED triage system. Please be calm. Everything will be fine.", lang="en")
    tts.save(audio_path)

# ---------- CONVERT AUDIO TO BASE64 ----------
import base64
with open(audio_path, "rb") as f:
    audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()

# ---------- AUTO-PLAYING AUDIO ----------
audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
"""

# ---------- FOOTER FIXED AT THE VERY BOTTOM ----------
st.markdown(
    """
    <div style="
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        color: gray;
        font-size: 14px;
        background-color: #ffffffaa;
        padding: 8px 0;
        backdrop-filter: blur(6px);">
        Thank you for using our AI-powered triage assistant.
    </div>
    """,
    unsafe_allow_html=True
)


# Reset functionality
if "reset" not in st.session_state:
    st.session_state.reset = False

if st.button("🔄 Reset Form"):
    st.session_state.clear()
    st.rerun()

# Patient demographics
st.header("👤 Patient Information")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
gender = st.radio("Gender", ["Male", "Female"])
diabetic = st.checkbox("Diabetic")
hypertensive = st.checkbox("Hypertensive")
smoker = st.checkbox("Smoker")
asthma = st.checkbox("Asthma")
allergies = st.checkbox("Allergies")
allergy_details = ""
if allergies:
    allergy_details = st.text_input("Please specify allergies")
medicine = st.text_input("Are you taking any regular medicine?")

# Main symptom selection
st.header("🤒 Main Symptom")
main_symptom = st.radio(
    "What is your main symptom?",
    ["Chest Pain", "Fever", "Abdominal Pain", "Women + Bleeding", "Accident + Wound"]
)

# Triage decision
decision = None
advice = ""

# ---------------- FLOWCHARTS ----------------

# 1. Chest Pain Flow
if main_symptom == "Chest Pain":
    st.subheader("Chest Pain Assessment")
    cp_pressure = st.checkbox("Is the chest pain pressure-like?")
    cp_breathing = st.checkbox("Does the pain increase with breathing or movement?")
    cp_duration = st.checkbox("Lasting more than 20 minutes?")
    cp_radiating = st.checkbox("Radiating to arm, neck, or jaw?")

    if cp_pressure:
        decision = "🔴 RED FLAG"
        advice = "🚨 Go immediately to **ECG Clinic**."
    elif cp_breathing:
        decision = "🟢 GREEN FLAG"
        advice = "✅ Do not worry, calm down. You are not in risk. Our triage physician will talk to you, but if you want ED you have to wait long times (hours)."
    elif cp_duration or cp_radiating:
        decision = "🔴 RED FLAG"
        advice = "🚨 You need urgent evaluation in the Emergency Department."
    else:
        decision = "🟢 GREEN FLAG"
        advice = "✅ Do not worry, calm down. You are not in risk. Our triage physician will talk to you, but if you want ED you have to wait long times (hours)."

# 2. Fever Flow
elif main_symptom == "Fever":
    st.subheader("Fever Assessment")
    temperature = st.number_input("🌡️ Body Temperature (°C)", min_value=35.0, max_value=42.0, step=0.1)
    severe_thirst = st.checkbox("Severe thirst?")
    sore_throat = st.checkbox("Sore throat?")
    headache = st.checkbox("Headache?")
    cough = st.checkbox("Cough?")
    muscle_ache = st.checkbox("Muscle ache?")
    heat_exposure = st.checkbox("Exposure to heat exhaustion?")

    if temperature >= 39 or severe_thirst or heat_exposure:
        decision = "🔴 RED FLAG"
        advice = "🚨 You need urgent evaluation in the Emergency Department."
    else:
        decision = "🟢 GREEN FLAG"
        advice = "✅ Do not worry, calm down. You are not in risk. Our triage physician will talk to you, but if you want ED you have to wait long times (hours)."

# 3. Abdominal Pain Flow
elif main_symptom == "Abdominal Pain":
    st.subheader("Abdominal Pain Assessment")
    severe_pain = st.checkbox("Severe abdominal pain?")
    vomiting = st.checkbox("Vomiting?")
    blood_stool = st.checkbox("Blood in stool?")
    urine_burn = st.checkbox("Burning sensation in urine?")
    urine_difficulty = st.checkbox("Difficulty or inability to urinate?")
    bad_food = st.checkbox("History of eating or drinking untrusted food?")

    if severe_pain or vomiting or blood_stool or urine_difficulty:
        decision = "🔴 RED FLAG"
        advice = "🚨 You need urgent evaluation in the Emergency Department."
    else:
        decision = "🟢 GREEN FLAG"
        advice = "✅ Do not worry, calm down. You are not in risk. Our triage physician will talk to you, but if you want ED you have to wait long times (hours)."

# 4. Women + Bleeding Flow
elif main_symptom == "Women + Bleeding":
    st.subheader("Women + Bleeding Assessment")
    pregnant = st.checkbox("Are you pregnant?")
    heavy_bleeding = st.checkbox("Heavy bleeding?")
    dizziness = st.checkbox("Dizziness or fainting?")
    severe_pain = st.checkbox("Severe abdominal pain?")

    if pregnant or heavy_bleeding or dizziness or severe_pain:
        decision = "🔴 RED FLAG"
        advice = "🚨 You need urgent evaluation in the Emergency Department."
    else:
        decision = "🟢 GREEN FLAG"
        advice = "✅ Do not worry, calm down. You are not in risk. Our triage physician will talk to you, but if you want ED you have to wait long times (hours)."

# 5. Accident + Wound Flow
elif main_symptom == "Accident + Wound":
    st.subheader("Accident + Wound Assessment")
    fracture = st.checkbox("Suspected fracture?")
    bleeding = st.checkbox("Active bleeding?")
    unconscious = st.checkbox("Unconscious?")
    severe_pain = st.checkbox("Severe pain?")

    if fracture or bleeding or unconscious or severe_pain:
        decision = "🔴 RED FLAG"
        advice = "🚨 Please visit **Block B2**. Your token number is **2907**. There are **2 patients waiting**."
    else:
        decision = "🟢 GREEN FLAG"
        advice = "✅ Do not worry, calm down. You are not in risk. Our triage physician will talk to you, but if you want ED you have to wait long times (hours)."

# ---------------- Show Result ----------------
if decision:
    st.subheader("📊 Triage Result")
    if "RED" in decision:
        st.error(f"{decision}\n\n{advice}")
    else:
        st.success(f"{decision}\n\n{advice}")
st.write("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Thank you for using our AI-powered triage assistant.</p>",
    unsafe_allow_html=True
)
if st.button("Reset"):
    for key in st.session_state.keys():
        st.session_state[key] = ""
    st.experimental_rerun()

