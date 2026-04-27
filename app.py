"""
Clinical Decision Support System
"""

import streamlit as st
import json
import os
from datetime import datetime
import re
import tempfile

st.set_page_config(page_title="GuidelinesIQ:Maternity", page_icon="🏥", layout="wide")

# CSS for small edit buttons
st.markdown("""
<style>
/* Small edit button style */
.small-edit-btn button {
    font-size: 12px !important;
    padding: 2px 8px !important;
    min-height: 0 !important;
    height: auto !important;
    line-height: 1.4 !important;
}
</style>
""", unsafe_allow_html=True)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
HISTORY_FILE = os.path.join(DATA_DIR, "conversation_history.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(fp, default):
    try:
        return json.load(open(fp)) if os.path.exists(fp) else default
    except:
        return default

def save_json(fp, data):
    json.dump(data, open(fp, 'w'), indent=2, default=str)

if "history" not in st.session_state:
    st.session_state.history = load_json(HISTORY_FILE, [])
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "scenario_text" not in st.session_state:
    st.session_state.scenario_text = ""
if "patient_data" not in st.session_state:
    st.session_state.patient_data = None
if "guidelines" not in st.session_state:
    st.session_state.guidelines = []
if "selected_actions" not in st.session_state:
    st.session_state.selected_actions = []
if "selected_tests" not in st.session_state:
    st.session_state.selected_tests = []
if "custom_weeks" not in st.session_state:
    st.session_state.custom_weeks = None
if "custom_conditions" not in st.session_state:
    st.session_state.custom_conditions = []
if "custom_free_text" not in st.session_state:
    st.session_state.custom_free_text = ""
if "last_audio_processed" not in st.session_state:
    st.session_state.last_audio_processed = None
if "audio_counter" not in st.session_state:
    st.session_state.audio_counter = 0

# Demo use cases
DEMO_USE_CASES = {
    "Select a use case...": "",
    "Use Case 1: Epilepsy + Lamotrigine": "24 year old with a history of epilepsy, last seizure 4 months ago, on lamotrigine, currently 16 weeks pregnant",
    "Use Case 2: High BMI + Previous SGA + Previous Caesarean": "40 year old, 28 weeks pregnant, BMI of 35 with a history of Caesarean section at 38 weeks for small baby 3 years ago",
    "Use Case 3: Previous Preterm": "29 year old, previous preterm labour at 30 weeks",
    "Use Case 4: High BMI + DVT": "42 year old, BMI of 45, Para 2 and previous history of DVT",
    "Use Case 5: Recurrent SGA (Para 2, Worsening Pattern)": "35 year old, Para 2, reviewing at 16 weeks. Previous baby 1: boy born at 37+2, weighing 2.8kg. Previous baby 2: boy born at 37+3, weighing 2.2kg.",
    "Use Case 6: Thrombocytopenia": "32 year old, reviewing at 30 weeks. Platelet count 60.",
    "Use Case 7: Previous Pre-eclampsia + Previous Caesarean + AMA": "40 year old, reviewing at 28 weeks. Previous pre-eclampsia and previous Caesarean section.",
}

# Patient leaflets database
PATIENT_LEAFLETS = {
    "pre-eclampsia": [
        {"title": "Pre-eclampsia", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/pre-eclampsia/"},
        {"title": "High blood pressure in pregnancy", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/related-conditions/complications/high-blood-pressure/"},
    ],
    "gestational_diabetes": [
        {"title": "Gestational diabetes", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/gestational-diabetes/"},
        {"title": "Gestational diabetes", "source": "NHS", "url": "https://www.nhs.uk/conditions/gestational-diabetes/"},
    ],
    "anaemia": [
        {"title": "Iron deficiency anaemia", "source": "NHS", "url": "https://www.nhs.uk/conditions/iron-deficiency-anaemia/"},
        {"title": "Vitamins and supplements in pregnancy", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/keeping-well/vitamins-supplements-and-nutrition/"},
    ],
    "twins": [
        {"title": "Multiple pregnancy (twins or more)", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/multiple-pregnancy-twins-or-more/"},
        {"title": "Pregnant with twins", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/finding-out/pregnant-with-twins/"},
    ],
    "sga": [
        {"title": "Having a small baby", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/having-a-small-baby/"},
        {"title": "Your baby's movements", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/your-babys-movements-in-pregnancy/"},
    ],
    "previous_caesarean": [
        {"title": "Birth after previous caesarean", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/birth-after-previous-caesarean/"},
        {"title": "Caesarean section", "source": "NHS", "url": "https://www.nhs.uk/conditions/caesarean-section/"},
    ],
    "obesity": [
        {"title": "Being overweight in pregnancy and after birth", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/being-overweight-in-pregnancy-and-after-birth/"},
        {"title": "Healthy eating in pregnancy", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/keeping-well/have-a-healthy-diet/"},
    ],
    "cholestasis": [
        {"title": "Intrahepatic cholestasis of pregnancy (ICP)", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/intrahepatic-cholestasis-of-pregnancy-icp/"},
        {"title": "Itching and intrahepatic cholestasis", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/related-conditions/complications/itching-and-intrahepatic-cholestasis/"},
    ],
    "thrombocytopenia": [
        {"title": "About ITP (Immune Thrombocytopenia)", "source": "ITP Support Association", "url": "https://itpsupport.org.uk/about-itp/"},
        {"title": "ITP in Pregnancy – UK Pregnancy Registry", "source": "ITP Support Association", "url": "https://itpsupport.org.uk/itp-in-pregnancy-registry/"},
        {"title": "ITP in Adults", "source": "ITP Support Association", "url": "https://itpsupport.org.uk/itp-in-adults/"},
    ],
    "vte": [
        {"title": "Reducing the risk of blood clots in pregnancy", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/reducing-the-risk-of-blood-clots-venous-thromboembolism-during-pregnancy-or-after-birth/"},
        {"title": "Blood clots in pregnancy", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/related-conditions/complications/blood-clot/"},
    ],
    "epilepsy": [
        {"title": "Epilepsy and pregnancy", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/epilepsy-and-pregnancy/"},
        {"title": "Epilepsy and pregnancy", "source": "Epilepsy Action", "url": "https://www.epilepsy.org.uk/info/women/pregnancy"},
    ],
    "breech": [
        {"title": "Turning your breech baby (ECV)", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/turning-your-breech-baby-ecv/"},
        {"title": "Breech baby at the end of pregnancy", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/labour-and-birth/what-happens/if-your-baby-is-breech/"},
    ],
    "reduced_movements": [
        {"title": "Your baby's movements in pregnancy", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/your-babys-movements-in-pregnancy/"},
        {"title": "Baby movements", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/keeping-well/your-babys-movements/"},
    ],
    "general": [
        {"title": "Pregnancy, birth and beyond", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-our-patient-information/"},
        {"title": "Your pregnancy care", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/your-pregnancy-care/"},
    ],
}

# Guideline URLs - National and Local
# SharePoint base for local Hillingdon/THH Maternity Guidelines
SHAREPOINT_BASE = "https://brunel365-my.sharepoint.com/my?id=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines%2F"
SHAREPOINT_FOLDER = "https://brunel365-my.sharepoint.com/my?id=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines&viewid=7bd060e2%2Db6c6%2D472d%2D8f8f%2D563d8d555b08"

GUIDELINE_URLS = {
    # National Guidelines - NICE (public links)
    "NG201": "https://www.nice.org.uk/guidance/ng201",  # Antenatal care
    "NG133": "https://www.nice.org.uk/guidance/ng133",  # Hypertension in pregnancy
    "NG3": "https://www.nice.org.uk/guidance/ng3",      # Diabetes in pregnancy
    "NG137": "https://www.nice.org.uk/guidance/ng137",  # Twin and triplet pregnancy
    "NG217": "https://www.nice.org.uk/guidance/ng217",  # Epilepsies in children, young people and adults
    "NG247": "https://www.nice.org.uk/guidance/ng247",  # Maternal and child nutrition
    "NG25": "https://www.nice.org.uk/guidance/ng25",    # Preterm labour and birth
    "NG192": "https://www.nice.org.uk/guidance/ng192",  # Caesarean birth
    "NG207": "https://www.nice.org.uk/guidance/ng207",  # Inducing labour
    # National Guidelines - RCOG Green-top (public links)
    "GTG68": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/epilepsy-in-pregnancy-green-top-guideline-no-68/",
    "GTG37a": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/reducing-the-risk-of-thrombosis-and-embolism-during-pregnancy-and-the-puerperium-green-top-guideline-no-37a/",
    "GTG37b": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/thrombosis-and-embolism-during-pregnancy-and-the-puerperium-acute-management-green-top-guideline-no-37b/",
    "GTG72": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/care-of-women-with-obesity-in-pregnancy-green-top-guideline-no-72/",
    "GTG31": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/small-for-gestational-age-fetus-investigation-and-management-green-top-guideline-no-31/",
    "GTG43": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/obstetric-cholestasis-green-top-guideline-no-43/",
    "GTG45": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/birth-after-previous-caesarean-birth-green-top-guideline-no-45/",
    # NHS England Guidelines
    "SBL3": "https://www.england.nhs.uk/long-read/saving-babies-lives-version-3/",  # Saving Babies' Lives Care Bundle Version 3
    # Local Guidelines (Hillingdon/THH) - Direct links from Antenatal Care Schedule
    "THH-Epilepsy": SHAREPOINT_BASE + "202405211452040.Epilepsy%20in%20pregnancy%20V7.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-FGR": SHAREPOINT_BASE + "202411210723400.FGR%20Guideline%202024%20Hillingdon%202024.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-BMI": SHAREPOINT_FOLDER + "&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",  # "Raised Body Mass Index (BMI) in pregnancy guideline" - no specific PDF found
    "THH-VBAC": SHAREPOINT_BASE + "202506241450060.Vaginal%20birth%20after%20csection%20VBAC%20V7.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-VTE": SHAREPOINT_FOLDER + "&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",  # VTE Prophylaxis flowchart in Antenatal Care Schedule
    "THH-PTB": SHAREPOINT_FOLDER + "&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",  # Preterm Birth Clinic Pathway
    "THH-ANC": SHAREPOINT_BASE + "202512191144050.Maternal%20Antenatal%20screening%20tests%20Guidelines%20v5.1.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-Anaemia": SHAREPOINT_BASE + "202511211517060.Anaemia%20and%20Ferinject%20Infusion%20in%20Pregnancy%20v3.1.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-GDM": SHAREPOINT_BASE + "202512191131340.gestational%20diabetes%20guideline%20v4.1.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-Hypertension": SHAREPOINT_BASE + "202601301510290.Antenatal%20Hypertension%20Pregnancy%20V5.1.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-Thyroid": SHAREPOINT_BASE + "202504141031280.Thyroid%20guideline%20V3.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    # Additional local guidelines from Antenatal Care Schedule
    "THH-Antibodies": SHAREPOINT_BASE + "202502241020400.Antibodies%20in%20pregnancy%20V5.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-SickleCell": SHAREPOINT_BASE + "202601231300520.Sickle%20Cell%20Disease%20and%20Pregnancy%20v5.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-Syphilis": SHAREPOINT_BASE + "202212011531480.Management%20of%20Positive%20Syphilis%20Serology%20in%20Pregnancy%20v.4.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-ChickenPox": SHAREPOINT_BASE + "202204111056350.Chicken%20pox%20in%20pregnancy.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-Herpes": SHAREPOINT_BASE + "202411110820540.Genital%20warts%20in%20pregnancy%20V5.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-LGA": SHAREPOINT_BASE + "202405211458230.Management%20of%20large%20for%20gestational%20age%20foetuses%20and%20macrosomia%20V2.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-Ultrasound": SHAREPOINT_BASE + "202507081315310.Obstetric_ultrasound%20protocol%20V4.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-MEWS": SHAREPOINT_BASE + "202506241703290.MEWS%20Early%20recognition%20of%20the%20severely%20ill%20pregnant%20woman%20V3.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
    "THH-Thrombocytopenia": SHAREPOINT_BASE + "202506271704420.thrombocytopenia%20in%20pregnancy%20v3.0.pdf&parent=%2Fpersonal%2Fcsstrrn%5Fbrunel%5Fac%5Fuk%2FDocuments%2FHealthHackathon%2DTeam5%2FMaternity%20clinical%20guidelines",
}

def make_link(ref):
    code = ref.split()[0] if ref else ""
    for key, url in GUIDELINE_URLS.items():
        if key in code:
            return f"[{ref}]({url})"
    return ref

def extract_weeks_from_timing(timing_str):
    """Extract gestational week number from timing string. Returns None if not a specific gestational week.
    Named periods are mapped to representative gestational weeks for filtering purposes.
    'Postnatal' and condition-based timings return None (always shown)."""
    timing_lower = timing_str.lower()
    # Postnatal / condition-based / ongoing → no gestational week, always relevant
    if re.search(r'postnatal|after\s+birth|after\s+delivery|if\s+|ongoing|urgent|as\s+indicated|as\s+needed', timing_lower):
        return None
    # Named gestational periods → map to last week of that period for filtering
    if re.search(r'\bbook(?:ing)?\b', timing_lower):
        return 10   # booking ~10 weeks
    if re.search(r'first\s+trimester', timing_lower):
        return 12
    if re.search(r'second\s+trimester', timing_lower):
        return 27
    # Match explicit week numbers: "16 weeks", "32w", "at 36 weeks", "28-32 weeks" (take first number)
    week_match = re.search(r'(\d+)\s*w(?:eeks?)?', timing_lower)
    if week_match:
        return int(week_match.group(1))
    return None

def transcribe_audio(audio_bytes):
    """Transcribe audio using OpenAI Whisper API"""
    tmp_file_path = None
    try:
        # Check if audio_bytes is valid
        if audio_bytes is None:
            return "⚠️ No audio data received"

        audio_data = audio_bytes.getvalue()
        if not audio_data or len(audio_data) < 100:
            return "⚠️ Audio recording too short"

        # Try to import openai
        try:
            from openai import OpenAI
        except ImportError:
            return "⚠️ OpenAI package not installed. Run: pip install openai"

        # Check for API key in environment or Streamlit secrets
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            try:
                if hasattr(st, "secrets") and "OPENAI_API_KEY" in st.secrets:
                    api_key = st.secrets["OPENAI_API_KEY"]
            except:
                pass  # Secrets file doesn't exist, that's ok

        if not api_key:
            return "⚠️ OpenAI API key not found. Please set OPENAI_API_KEY environment variable or add to .streamlit/secrets.toml"

        # Create OpenAI client
        client = OpenAI(api_key=api_key)

        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data)
            tmp_file_path = tmp_file.name

        # Transcribe using Whisper
        with open(tmp_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text if transcript and transcript.text else "⚠️ No speech detected"

    except Exception as e:
        return f"⚠️ Transcription error: {str(e)}"
    finally:
        # Clean up temporary file
        if tmp_file_path and os.path.exists(tmp_file_path):
            try:
                os.unlink(tmp_file_path)
            except:
                pass

# Approximate 10th centile birthweight thresholds (grams) by completed gestation week and sex
# Based on UK-WHO/GROW growth charts. Used for automatic SGA detection from birth history.
_SGA_10TH_CENTILE = {
    # week: (male_g, female_g)
    28: (800, 760),   29: (930, 885),   30: (1065, 1015), 31: (1220, 1165),
    32: (1400, 1340), 33: (1600, 1530), 34: (1810, 1740), 35: (2045, 1965),
    36: (2290, 2205), 37: (2530, 2440), 38: (2720, 2625), 39: (2895, 2800),
    40: (3055, 2960), 41: (3195, 3100), 42: (3310, 3215),
}

def _is_sga(weight_g, gestation_weeks, sex="unknown"):
    """Return True if birthweight < 10th centile for gestation and sex (UK-WHO/GROW)."""
    week = min(max(int(gestation_weeks), 28), 42)
    male_thresh, female_thresh = _SGA_10TH_CENTILE.get(week, _SGA_10TH_CENTILE[40])
    if sex == "male":
        return weight_g < male_thresh
    elif sex == "female":
        return weight_g < female_thresh
    return weight_g < (male_thresh + female_thresh) // 2

def parse_scenario(text):
    """Parse free text scenario into structured data"""
    text_lower = text.lower()
    data = {"age": None, "weeks": None, "parity": None, "bmi": None, "risks": [], "labs": {}, "leaflet_tags": []}

    # Age (handles "24yo", "24 year old", "40-year-old" from audio transcription)
    age_match = re.search(r'(\d+)\s*-?\s*(?:year|yr|y/?o)', text_lower)
    if age_match:
        data["age"] = int(age_match.group(1))

    # Weeks
    weeks_match = re.search(r'(\d+)\s*weeks?', text_lower)
    if weeks_match:
        data["weeks"] = int(weeks_match.group(1))

    # Platelet count
    platelet_match = re.search(r'platelet(?:s|\s+count)?\s*(?:of\s*)?(\d+)', text_lower)
    if platelet_match:
        platelets = int(platelet_match.group(1))
        data["labs"]["platelets"] = platelets
        if platelets < 150:
            if "Thrombocytopenia" not in data["risks"]:
                data["risks"].append("Thrombocytopenia")
            if "thrombocytopenia" not in data["leaflet_tags"]:
                data["leaflet_tags"].append("thrombocytopenia")

    # BMI
    bmi_match = re.search(r'bmi\s*(?:of\s*)?(\d+(?:\.\d+)?)', text_lower)
    if bmi_match:
        data["bmi"] = float(bmi_match.group(1))
        data["labs"]["BMI"] = data["bmi"]
        if data["bmi"] >= 30:
            data["risks"].append(f"BMI {data['bmi']}")
            data["leaflet_tags"].append("obesity")

    # Parity
    para_match = re.search(r'para\s*(\d+)|p(\d+)|g(\d+)p(\d+)', text_lower)
    if para_match:
        if para_match.group(1):
            data["parity"] = f"P{para_match.group(1)}"
        elif para_match.group(4):
            data["parity"] = f"G{para_match.group(3)}P{para_match.group(4)}"

    # Conditions with leaflet tags
    conditions = [
        ("epilepsy", "Epilepsy", "epilepsy"), ("lamotrigine", "On Lamotrigine", "epilepsy"),
        ("dvt", "Previous VTE", "vte"), ("thrombosis", "Previous VTE", "vte"),
        ("preterm", "Previous preterm", None),
        ("sga", "Previous SGA", "sga"), ("small baby", "Previous SGA", "sga"), ("fgr", "Previous FGR", "sga"),
        ("caesarean", "Previous Caesarean", "previous_caesarean"), ("c-section", "Previous Caesarean", "previous_caesarean"),
        ("pre-eclampsia", "Previous pre-eclampsia", "pre-eclampsia"), ("preeclampsia", "Previous pre-eclampsia", "pre-eclampsia"),
        ("cholestasis", "Obstetric Cholestasis", "cholestasis"), ("itching", "? Obstetric Cholestasis", "cholestasis"),
        ("thrombocytopenia", "Thrombocytopenia", "thrombocytopenia"), ("low platelets", "Thrombocytopenia", "thrombocytopenia"),
        ("anaemia", "Anaemia", "anaemia"), ("anemia", "Anaemia", "anaemia"),
        ("twins", "Twins", "twins"), ("multiple", "Multiple pregnancy", "twins"),
        ("breech", "Breech", "breech"), ("reduced movement", "Reduced movements", "reduced_movements"),
        ("gdm", "GDM", "gestational_diabetes"), ("gestational diabetes", "GDM", "gestational_diabetes"),
    ]
    for keyword, risk, leaflet_tag in conditions:
        if keyword in text_lower:
            if risk not in data["risks"]:
                data["risks"].append(risk)
            if leaflet_tag and leaflet_tag not in data["leaflet_tags"]:
                data["leaflet_tags"].append(leaflet_tag)

    # Previous birth history - auto-detect SGA from weight + gestation centile lookup
    # Matches: "born at 37+2, weighing 2.8kg" / "at 37+3 weighing 2200g" etc.
    sex_in_text = "male" if re.search(r'\bboy\b|\bsons?\b', text_lower) else \
                  ("female" if re.search(r'\bgirl\b|\bdaughters?\b', text_lower) else "unknown")
    birth_records = re.findall(
        r'born\s+at\s+(\d+)(?:\+(\d+))?\s*,?\s*(?:weeks?)?\s*,?\s*(?:weighing|weigh(?:ed|s)?|weight(?:\s+of)?|wt\.?)?\s*(\d+(?:\.\d+)?)\s*(kg|g\b)',
        text_lower
    )
    for record in birth_records:
        gestation_weeks = int(record[0]) + (int(record[1]) / 7 if record[1] else 0)
        weight_val = float(record[2])
        weight_g = weight_val * 1000 if record[3] == "kg" else weight_val
        if _is_sga(weight_g, gestation_weeks, sex_in_text):
            if "Previous SGA" not in data["risks"]:
                data["risks"].append("Previous SGA")
            if "sga" not in data["leaflet_tags"]:
                data["leaflet_tags"].append("sga")

    return data

def get_applicable_guidelines(patient_data, risks_text):
    """Get guidelines based on conditions - aligned with THH Antenatal Care Schedule"""
    guidelines = []
    # Include auto-detected risks (e.g. SGA from centile check) alongside raw text
    parsed_risks = " ".join(patient_data.get("risks", [])).lower()
    combined = risks_text.lower() + " " + parsed_risks
    labs = patient_data.get("labs", {})
    weeks = patient_data.get("weeks") or 20  # Default to 20 if None
    age = patient_data.get("age")

    # Previous SGA/FGR (small baby) - GTG31, Saving Babies Lives v3, THH FGR Guideline
    if "previous sga" in combined or "small baby" in combined or "previous fgr" in combined:
        guidelines.append({
            "name": "Previous SGA/FGR",
            "code": "THH-FGR",
            "summary": "Risk of recurrence. Follow THH FGR Guideline + GTG31 + Saving Babies Lives v3. Aspirin 150mg, uterine artery Dopplers, serial growth scans. IOL at 39/40.",
            "actions": [
                {"text": "Aspirin 150mg from 12 weeks (if <20w) to reduce recurrence risk", "ref": "THH-FGR", "default": False},
                {"text": "Assess risk factors for FGR using RCOG stratification", "ref": "GTG31", "default": False},
                {"text": "Implement Saving Babies Lives v3 growth surveillance pathway", "ref": "SBL3", "default": False},
                {"text": "Customised growth charts (GROW) per SBL3 Element 2", "ref": "SBL3", "default": False},
                {"text": "Follow local THH FGR pathway for monitoring schedule", "ref": "THH-FGR", "default": False}
            ],
            "tests": [
                {"text": "Uterine artery Doppler (pulsatility index)", "timing": "20-24 weeks", "ref": "THH-FGR"},
                {"text": "Umbilical artery Doppler if growth concern", "timing": "As indicated", "ref": "GTG31"}
            ],
            "ultrasound": [
                {"text": "Serial growth scans 4-weekly", "timing": "From 28 weeks till birth", "ref": "THH-FGR"}
            ],
            "followup": [
                {"text": "Consultant-led care per THH pathway", "timing": "Ongoing", "ref": "THH-FGR"},
                {"text": "Fetal Medicine referral if EFW <3rd centile", "timing": "If needed", "ref": "THH-FGR"}
            ],
            "clarify": [
                "What were the birthweights and gestations of all previous SGA babies? Was there a worsening pattern between pregnancies?",
                "Was there placental dysfunction (abruption, pre-eclampsia) in previous pregnancies?",
                "Were uterine artery Dopplers abnormal previously?",
                "Was PAPP-A low at first trimester screening in previous pregnancies? (marker of placental insufficiency)",
                "Is the patient already on Aspirin 150mg? If not, start now - still eligible at <20 weeks (GTG31)"
            ],
            "decisions": [
                {"question": "Number of previous SGA pregnancies?", "options": ["1 previous SGA → standard surveillance (THH-FGR)", "2+ previous SGA (recurrent) → higher recurrence risk, ensure Aspirin started, consider earlier Dopplers at 20w anomaly scan"]},
                {"question": "EFW at anomaly scan?", "options": ["≥10th centile → serial scans from 28w (THH-FGR)", "<10th centile → FGR pathway (GTG31)"]}
            ],
            "plan": [
                (12, "Start Aspirin 150mg if not already"),
                (20, "Uterine artery Dopplers at anomaly scan (THH-FGR)"),
                (28, "Growth scan - start serial monitoring"),
                (32, "Growth scan (THH-FGR)"),
                (36, "Growth scan + plan delivery"),
                (39, "Plan IOL unless other concerns")
            ]
        })

    # Current SGA - THH-FGR, GTG31, Saving Babies Lives v3
    if "current sga" in combined or "small for dates" in combined:
        guidelines.append({
            "name": "Current SGA/FGR",
            "code": "THH-FGR",
            "summary": "EFW/AC <10th centile. Follow THH FGR pathway + GTG31 + Saving Babies Lives v3 with serial Dopplers.",
            "actions": [
                {"text": "Classify severity: <10th centile (SGA) vs <3rd centile (severe FGR)", "ref": "GTG31", "default": False},
                {"text": "Document on GROW chart per SBL3 Element 2", "ref": "SBL3", "default": False},
                {"text": "Follow THH FGR pathway for local management", "ref": "THH-FGR", "default": False}
            ],
            "tests": [
                {"text": "Umbilical artery Doppler", "timing": "Serial monitoring", "ref": "THH-FGR"},
                {"text": "MCA Doppler if UA abnormal", "timing": "As indicated", "ref": "GTG31"}
            ],
            "ultrasound": [{"text": "Growth + Dopplers", "timing": "2-weekly if <10th, weekly if <3rd", "ref": "THH-FGR"}],
            "followup": [
                {"text": "Fetal medicine referral if <3rd centile or abnormal Dopplers", "timing": "Urgent", "ref": "THH-FGR"},
                {"text": "Consultant-led care with delivery planning", "timing": "Ongoing", "ref": "THH-FGR"}
            ],
            "decisions": [
                {"question": "EFW centile?", "options": ["3rd-10th → 2-weekly scans, IOL 37-39w (THH-FGR)", "<3rd → weekly scans, fetal medicine, IOL 37w"]},
                {"question": "Umbilical artery Doppler?", "options": ["Normal → continue surveillance", "Raised PI → increase monitoring", "AEDF/REDF → urgent fetal medicine, consider delivery"]}
            ],
            "plan": [(weeks, "FGR pathway assessment (THH-FGR)"), (weeks+1, "Repeat scan + Dopplers"), (37, "Delivery planning if severe FGR"), (39, "IOL if SGA")]
        })

    # Anaemia - THH Anaemia and Ferinject guideline
    if "anaemia" in combined or "anemia" in combined:
        guidelines.append({
            "name": "Anaemia in Pregnancy",
            "code": "THH-ANC",
            "summary": "1st trimester <110g/l, 2nd/3rd <105g/l. Oral iron first line, Ferinject if not tolerating.",
            "actions": [
                {"text": "Start oral iron (unless haemoglobinopathy - check ferritin first)", "ref": "THH-ANC", "default": False},
                {"text": "Ferinject if not tolerating orally", "ref": "THH-ANC", "default": False},
                {"text": "ANC referral if Hb<70g/l or symptomatic", "ref": "THH-ANC", "default": False}
            ],
            "tests": [
                {"text": "Booking, 28- and 34-weeks bloods", "timing": "As scheduled", "ref": "THH-ANC"},
                {"text": "Serum ferritin and haematinics if indicated", "timing": "Now", "ref": "THH-ANC"}
            ],
            "ultrasound": [{"text": "Scans if Hb<80g/l", "timing": "4-weekly till birth", "ref": "THH-ANC"}],
            "plan": [(weeks+2, "Repeat FBC"), (weeks+4, "Review response")]
        })

    # Pre-eclampsia Risk - THH Antenatal Hypertension guideline + NICE NG133
    if "pre-eclampsia" in combined or "preeclampsia" in combined or "previous pet" in combined:
        guidelines.append({
            "name": "Previous Pre-eclampsia",
            "code": "THH-Hypertension",
            "summary": "Previous PE = high risk of recurrence. Aspirin 150mg from 12w. Digital BP at all visits. Surveillance pathway determined by UA Doppler + EFW at 20w anomaly scan: normal UA+EFW → scans from 32w; abnormal UA → scans from 28w; EFW <10th → FMU referral. Deliver 37-38w if uncomplicated.",
            "actions": [
                {"text": "Confirm patient is on Aspirin 150mg daily (start now if not yet prescribed and <16w; review if >16w)", "ref": "NG133", "default": True},
                {"text": "Use digital BP at all antenatal appointments", "ref": "THH-Hypertension", "default": True},
                {"text": "Ensure consultant-led care is established", "ref": "THH-Hypertension", "default": True},
                {"text": "Advise patient on warning symptoms: severe headache, visual disturbance, epigastric pain, sudden oedema", "ref": "NG133", "default": False},
                {"text": "Complete 28-week bloods: FBC, U&E, LFTs, uric acid (if not yet done)", "ref": "THH-Hypertension", "default": True},
            ],
            "tests": [
                {"text": "BP and urinalysis (protein) at every antenatal visit", "timing": "Every 2-4 weeks", "ref": "THH-Hypertension"},
                {"text": "FBC, U&E, LFTs, uric acid", "timing": "28 weeks and 34 weeks", "ref": "THH-Hypertension"},
                {"text": "Urine PCR if proteinuria 1+ or more on dipstick", "timing": "As indicated", "ref": "NG133"},
                {"text": "Pre-eclampsia bloods (FBC, U&E, LFTs, clotting) if symptoms develop", "timing": "If symptomatic", "ref": "NG133"},
            ],
            "ultrasound": [
                {"text": "Uterine artery Doppler + anomaly scan (determines entire surveillance pathway)", "timing": "20 weeks", "ref": "THH-Hypertension"},
                {"text": "Serial growth scans every 2-4 weeks — if abnormal UA PI + EFW >10th centile at anomaly scan", "timing": "From 28 weeks", "ref": "THH-Hypertension"},
                {"text": "Serial growth scans — if normal UA PI + EFW >10th centile at anomaly scan", "timing": "From 32 weeks", "ref": "THH-Hypertension"},
                {"text": "Individualised serial growth scans — if normal UA PI + EFW <10th centile (discuss with FMU)", "timing": "From 26 weeks", "ref": "THH-Hypertension"},
            ],
            "followup": [
                {"text": "Consultant-led antenatal care throughout", "timing": "Ongoing", "ref": "THH-Hypertension"},
                {"text": "Maternal medicine referral if previous early-onset (<34w), severe PE, HELLP, or eclampsia", "timing": "Ongoing", "ref": "THH-Hypertension"},
                {"text": "Obstetric review and delivery planning", "timing": "36 weeks", "ref": "NG133"},
            ],
            "clarify": [
                "How severe was the previous pre-eclampsia? Early-onset (<34w), late-onset (>34w), HELLP, or eclampsia?",
                "At what gestation was the previous PE diagnosed and delivery planned?",
                "Is the patient currently on Aspirin 150mg? If so, when was it started?",
                "What is the current BP? Any symptoms (headache, visual disturbance, epigastric pain, oedema)?",
                "What were the uterine artery Doppler results at 20 weeks?",
                "Any co-existing conditions increasing PE risk (renal disease, diabetes, autoimmune, APS)?",
            ],
            "decisions": [
                {"question": "Severity of previous pre-eclampsia?", "options": [
                    "Late-onset (>34w), uncomplicated → aspirin, growth scans 28/32/36w, deliver 37-38w",
                    "Early-onset (<34w) or HELLP/eclampsia → maternal medicine referral, intensive surveillance from 24w",
                ]},
                {"question": "UA Doppler + EFW at 20-week anomaly scan? (THH-Hypertension pathway)", "options": [
                    "Normal UA PI + EFW >10th centile → serial growth scans from 32w",
                    "Abnormal UA PI + EFW >10th centile → serial growth scans from 28w (every 2-4 weeks)",
                    "Normal UA PI + EFW <10th centile → individualised serial scans from 26-28w",
                    "Abnormal UA PI + EFW <10th centile → FMU referral",
                ]},
                {"question": "BP ≥140/90 at any visit?", "options": [
                    "Yes → admit/day unit assessment, pre-eclampsia bloods, senior review per THH-Hypertension",
                    "No → continue 2-4 weekly monitoring",
                ]},
                {"question": "Proteinuria ≥1+ on dipstick?", "options": [
                    "Yes → send urine PCR; if PCR ≥30mg/mmol → investigate for pre-eclampsia",
                    "No → continue surveillance",
                ]},
            ],
            "plan": [
                (12, "Aspirin 150mg daily; Obstetric ANC within 2 weeks of booking (THH-Hypertension)"),
                (20, "UA Doppler + anomaly scan → determines growth scan pathway"),
                (26, "Growth scan if EFW <10th at 20w (individualised, discuss with FMU)"),
                (28, "Growth scan + 28w bloods (FBC, U&E, LFTs) — if abnormal UA Doppler"),
                (32, "Growth scan + Obs ANC — all pathways converge here"),
                (34, "34w bloods (FBC, U&E, LFTs, uric acid)"),
                (36, "Growth scan + delivery planning; aim delivery 37-38w if uncomplicated"),
                (37, "Consider delivery; no later than 38w unless clinical reason"),
            ]
        })

    # Obstetric Cholestasis
    if "cholestasis" in combined:
        guidelines.append({
            "name": "Obstetric Cholestasis",
            "code": "GTG43",
            "summary": "Bile acids monitoring, ursodeoxycholic acid, delivery planning.",
            "actions": [
                {"text": "Start Ursodeoxycholic acid", "ref": "GTG43", "default": False},
                {"text": "Vitamin K if prolonged PT", "ref": "GTG43", "default": False}
            ],
            "tests": [
                {"text": "Bile acids", "timing": "Weekly", "ref": "GTG43"},
                {"text": "LFTs", "timing": "Weekly", "ref": "GTG43"}
            ],
            "followup": [{"text": "Consultant-led care", "timing": "Ongoing", "ref": "GTG43"}],
            "plan": [(weeks, "Weekly bile acids + LFTs"), (37, "Consider delivery if bile acids >100")]
        })

    # Twins - THH Twin pregnancy guidelines
    if "twins" in combined or "multiple" in combined:
        guidelines.append({
            "name": "Multiple Pregnancy",
            "code": "THH-ANC",
            "summary": "Specialist team. DCDA: 4-weekly from 24w, deliver 37w. MCDA: 2-weekly from 16w, deliver 36w.",
            "actions": [
                {"text": "Folic acid 5mg throughout pregnancy", "ref": "THH-ANC", "default": False},
                {"text": "Consider Vitamin D", "ref": "THH-ANC", "default": False},
                {"text": "Aspirin if another risk factor present", "ref": "THH-ANC", "default": False}
            ],
            "tests": [
                {"text": "BP and urine at 20, 24, 28w then 2-weekly", "timing": "As scheduled", "ref": "THH-ANC"},
                {"text": "FBC at 24, 28 and 34 weeks", "timing": "As scheduled", "ref": "THH-ANC"}
            ],
            "ultrasound": [
                {"text": "Dating scan incl chorionicity, NT", "timing": "11-14 weeks", "ref": "NG137"},
                {"text": "DCDA: 4-weekly growth from 24w", "timing": "Deliver 37w", "ref": "THH-ANC"},
                {"text": "MCDA: 2-weekly from 16w (TTTS check)", "timing": "Deliver 36w", "ref": "THH-ANC"}
            ],
            "followup": [
                {"text": "Signpost to TAMBA and MBF websites", "timing": "At booking", "ref": "THH-ANC"},
                {"text": "Infant feeding and anaesthetist referral", "timing": "28 weeks", "ref": "THH-ANC"}
            ],
            "plan": [(16, "FMU referral if MCDA"), (24, "Start regular growth scans"), (28, "Anaesthetic/feeding referral"), (34, "Mode of birth discussion")]
        })

    # Thrombocytopenia - THH Thrombocytopenia in Pregnancy v3.0
    if "thrombocytopenia" in combined or "low platelets" in combined:
        platelets = labs.get("platelets")

        # Build severity-specific summary
        if platelets is not None:
            if platelets < 20:
                sev_note = f"Platelets {platelets} — SEVERE: treatment required to reduce risk of spontaneous haemorrhage. Regional anaesthesia contraindicated."
            elif platelets < 30:
                sev_note = f"Platelets {platelets} — SEVERE: treatment required to raise count >80 before delivery. Regional anaesthesia contraindicated."
            elif platelets < 50:
                sev_note = f"Platelets {platelets} — MODERATE: regional anaesthesia and major operative procedures contraindicated. Aspirin/NSAIDs contraindicated."
            elif platelets < 80:
                sev_note = f"Platelets {platelets} — MODERATE: regional anaesthesia must be discussed with anaesthetist. Full investigation required. Gestational thrombocytopenia unlikely (<80 warrants rethink of diagnosis)."
            elif platelets < 100:
                sev_note = f"Platelets {platelets} — MILD: anaesthetic referral required. Monitor fortnightly from 34w."
            else:
                sev_note = f"Platelets {platelets} — below normal range. Monitor."
        else:
            sev_note = "Platelet count below normal. Confirm on repeat FBC + blood film and classify severity."

        # Severity-dependent actions
        actions = [
            {"text": "Repeat FBC with blood film to confirm true thrombocytopenia (exclude spurious result)", "ref": "THH-Thrombocytopenia", "default": True},
            {"text": "Refer to joint obstetric haematology clinic", "ref": "THH-Thrombocytopenia", "default": platelets is not None and platelets < 80},
            {"text": "Anaesthetic referral - discuss regional and general anaesthesia options", "ref": "THH-Thrombocytopenia", "default": platelets is not None and platelets < 100},
            {"text": "Check: avoid aspirin and NSAIDs if platelets <50", "ref": "THH-Thrombocytopenia", "default": platelets is not None and platelets < 50},
            {"text": "Document management plan clearly in hospital and handheld notes (labour page)", "ref": "THH-Thrombocytopenia", "default": False},
            {"text": "Counsel re: presenting immediately if bleeding or bruising develops", "ref": "THH-Thrombocytopenia", "default": False},
        ]
        if platelets is not None and platelets < 50:
            actions.append({"text": "URGENT: If platelets <50 with bleeding/bruising, discuss immediately with on-call haematology registrar (bleep 5083)", "ref": "THH-Thrombocytopenia", "default": True})
        if platelets is not None and platelets < 30:
            actions.append({"text": "Treatment required (IVIg and/or corticosteroids) to raise platelets >80 before delivery - discuss with obstetric haematology", "ref": "THH-Thrombocytopenia", "default": True})

        guidelines.append({
            "name": "Thrombocytopenia in Pregnancy",
            "code": "THH-Thrombocytopenia",
            "summary": sev_note + " Most common cause: gestational thrombocytopenia (75%). ITP accounts for 3%. Full investigation if <80.",
            "actions": actions,
            "tests": [
                {"text": "FBC + blood film (confirm true thrombocytopenia, exclude spurious)", "timing": "Now", "ref": "THH-Thrombocytopenia"},
                {"text": "Reticulocyte count", "timing": "Now", "ref": "THH-Thrombocytopenia"},
                {"text": "LFTs, TFTs, DAT (direct antiglobulin test)", "timing": "If platelets <80", "ref": "THH-Thrombocytopenia"},
                {"text": "Antiphospholipid antibodies (APS ab) + ANA", "timing": "If platelets <80", "ref": "THH-Thrombocytopenia"},
                {"text": "HIV, Hepatitis B and C", "timing": "If platelets <80", "ref": "THH-Thrombocytopenia"},
                {"text": "H. pylori screen", "timing": "If platelets <80", "ref": "THH-Thrombocytopenia"},
                {"text": "Consider VWF testing (vWF:RCo, Ag and RIPA) to exclude VWF Type IIb", "timing": "If platelets <80", "ref": "THH-Thrombocytopenia"},
                {"text": "FBC fortnightly from 34 weeks if platelets <100", "timing": "From 34 weeks", "ref": "THH-Thrombocytopenia"},
                {"text": "FBC weekly after 34w if platelets falling below 80", "timing": "From 34 weeks if deteriorating", "ref": "THH-Thrombocytopenia"},
                {"text": "FBC on admission in labour or for planned delivery", "timing": "Intrapartum", "ref": "THH-Thrombocytopenia"},
            ],
            "ultrasound": [],
            "followup": [
                {"text": "Joint obstetric haematology clinic (monthly)", "timing": "If platelets <80", "ref": "THH-Thrombocytopenia"},
                {"text": "Anaesthetic referral (regional and general anaesthesia planning)", "timing": "If platelets <100", "ref": "THH-Thrombocytopenia"},
                {"text": "Postnatal haematology outpatient referral (at 8-12 weeks after birth) if thrombocytopenia persists", "timing": "Postnatal", "ref": "THH-Thrombocytopenia"},
            ],
            "clarify": [
                "What is the current platelet count and trend (rising, stable, or falling)?",
                "Any history of thrombocytopenia outside of pregnancy, or in previous pregnancies?",
                "Any bleeding, bruising, or petechiae?",
                "Any family history of thrombocytopenia or bleeding disorders?",
                "Current medications - particularly heparin, sodium valproate, aspirin, NSAIDs?",
                "Any symptoms of pre-eclampsia (headache, visual disturbance, epigastric pain, oedema)?",
                "Any symptoms suggesting infection (fever, malaise)?",
                "Has a repeat FBC + blood film been done to exclude spurious result?",
            ],
            "decisions": [
                {"question": "Platelet count threshold?", "options": [
                    ">100 → gestational thrombocytopenia likely, monitor fortnightly from 34w",
                    "80-100 → anaesthetic referral; fortnightly FBC from 34w; rethink if falling",
                    "<80 → full investigation, obstetric haematology clinic, anaesthetic referral, rethink diagnosis",
                    "<50 → regional anaesthesia + major procedures contraindicated; aspirin/NSAIDs contraindicated",
                    "<30 → treatment required before delivery (IVIg/steroids to raise >80)",
                    "<20 → treat to reduce risk of spontaneous haemorrhage",
                ]},
                {"question": "Features of ITP vs gestational thrombocytopenia?", "options": [
                    "Gestational: onset mid-2nd/3rd trimester, usually >70, no bleeding hx, normal film, no other cause",
                    "ITP: count <100 early in pregnancy, can be <5-10, responds to IVIg/steroids, fetal risk ~10% <50",
                    "If <50 → gestational thrombocytopenia very unlikely - investigate for ITP/other cause",
                ]},
                {"question": "Intrapartum precautions if platelets <100 or previous ITP?", "options": [
                    "Avoid: fetal blood sampling, fetal scalp electrodes, high forceps, ventouse delivery",
                    "Mode of delivery determined by obstetric indications, not platelet count alone",
                ]},
                {"question": "Neonatal risk if ITP suspected?", "options": [
                    "~10% of babies have platelets <50, 5% have <20 → peripheral blood sample at delivery",
                    "Recheck daily if thrombocytopenic (nadir at 2-5 days)",
                    "Cranial USS if neonatal platelets <50 (ICH risk)",
                ]},
            ],
            "plan": [
                (weeks, "Repeat FBC + blood film; refer obstetric haematology if <80"),
                (weeks, "Anaesthetic referral if platelets <100"),
                (34, "FBC fortnightly if platelets <100; weekly if <80 and falling"),
                (34, "Review intrapartum precautions; document in notes"),
                (36, "Delivery planning: confirm platelet count, anaesthetic plan, intrapartum instructions"),
                (40, "FBC on admission in labour; postnatal haematology referral if persists"),
            ]
        })

    # VTE / Previous DVT - THH VTE Prophylaxis flowchart
    if "dvt" in combined or "vte" in combined or "thrombosis" in combined:
        guidelines.append({
            "name": "Previous VTE - HIGH RISK",
            "code": "THH-VTE",
            "summary": "Any previous VTE = HIGH RISK. Requires antenatal LMWH prophylaxis. Refer to thrombosis expert.",
            "actions": [
                {"text": "Start antenatal prophylaxis with LMWH", "ref": "THH-VTE", "default": False},
                {"text": "At least 6 weeks postnatal prophylactic LMWH", "ref": "THH-VTE", "default": False}
            ],
            "tests": [{"text": "Thrombophilia screen (if not previously done)", "timing": "At booking", "ref": "GTG37a"}],
            "followup": [
                {"text": "Thrombosis in pregnancy expert/team referral", "timing": "At booking", "ref": "THH-VTE"},
                {"text": "Haematology review", "timing": "First trimester", "ref": "THH-VTE"}
            ],
            "clarify": [
                "Was the previous VTE provoked or unprovoked?",
                "Was it related to pregnancy, surgery, or immobility?",
                "Has thrombophilia screening been done? Results?",
                "Is patient currently on anticoagulation?"
            ],
            "decisions": [
                {"question": "VTE type?", "options": ["Unprovoked/recurrent → HIGH RISK, LMWH throughout", "Single provoked (non-pregnancy) → consider intermediate risk"]}
            ],
            "plan": [
                (weeks, "Start/continue LMWH prophylaxis"),
                (36, "Delivery planning: LMWH timing, regional anaesthesia"),
                (40, "Postnatal: 6 weeks LMWH prophylaxis")
            ]
        })

    # Epilepsy - THH Epilepsy in pregnancy V7
    if "epilepsy" in combined or "lamotrigine" in combined or "seizure" in combined:
        guidelines.append({
            "name": "Epilepsy in Pregnancy",
            "code": "THH-Epilepsy",
            "summary": "Folic acid 5mg preconception. Refer to Obs Med. Detailed anomaly + ECHO. 4-weekly growth from 28w.",
            "actions": [
                {"text": "Folic acid 5mg daily (preconception)", "ref": "THH-Epilepsy", "default": False},
                {"text": "Register on UK Epilepsy and Pregnancy Register", "ref": "THH-Epilepsy", "default": False}
            ],
            "tests": [
                {"text": "Drug levels only if seizure frequency increases or dose change", "timing": "As needed", "ref": "THH-Epilepsy"}
            ],
            "ultrasound": [
                {"text": "Detailed anomaly scan + ECHO", "timing": "20 weeks", "ref": "THH-Epilepsy"},
                {"text": "4-weekly growth scans (sonographer-led FMU)", "timing": "From 28 weeks", "ref": "THH-Epilepsy"}
            ],
            "followup": [
                {"text": "Obs Med team referral", "timing": "At booking", "ref": "THH-Epilepsy"},
                {"text": "Joint Obstetric-Neurology care", "timing": "Ongoing", "ref": "THH-Epilepsy"}
            ],
            "clarify": [
                "What AED (anti-epileptic drug) is patient on? Dose?",
                "When was the last seizure?",
                "What type of seizures (focal, generalised, tonic-clonic)?",
                "Has patient been taking folic acid 5mg preconception?",
                "Any previous pregnancies on AEDs? Outcomes?"
            ],
            "decisions": [
                {"question": "Seizure frequency increasing?", "options": ["Yes → check drug levels, neurology review", "No → continue current dose, no levels needed"]},
                {"question": "On enzyme-inducing AED?", "options": ["Yes → Vitamin K 10mg daily from 36w", "No → routine Vitamin K advice"]}
            ],
            "plan": [
                (16, "Obs ANC: review seizure control, SUDEP risk"),
                (20, "Detailed anomaly scan + fetal ECHO"),
                (28, "Growth scan; Obs +/- Neuro review"),
                (32, "Obs ANC: Vitamin K discussion"),
                (36, "Birth planning, postnatal contraception")
            ]
        })

    # High BMI - THH Raised BMI guideline
    if labs.get("BMI") and labs["BMI"] >= 35:
        bmi = labs["BMI"]
        if bmi >= 40:
            guidelines.append({
                "name": "BMI ≥40 (Class III Obesity)",
                "code": "THH-BMI",
                "summary": f"BMI {bmi}. HIGH VTE RISK. LMWH from first trimester. Anaesthetic review at 32w. OGTT 24-28w.",
                "actions": [
                    {"text": "Folic acid 5mg preconception", "ref": "THH-BMI", "default": False},
                    {"text": "VTE and FGR risk assessment at booking", "ref": "THH-BMI", "default": False},
                    {"text": "Vitamin D 25mcg or 1000IU", "ref": "THH-BMI", "default": False},
                    {"text": "Start LMWH (4+ risk factors = from first trimester)", "ref": "THH-VTE", "default": False},
                    {"text": "Assess if equipment can adjust to patient", "ref": "THH-BMI", "default": False}
                ],
                "tests": [
                    {"text": "OGTT 75g", "timing": "24-28 weeks", "ref": "NG3"},
                    {"text": "Appropriate cuff size for BP", "timing": "All visits", "ref": "THH-BMI"}
                ],
                "ultrasound": [{"text": "4-weekly growth scans", "timing": "From 32 weeks till birth", "ref": "THH-BMI"}],
                "followup": [
                    {"text": "Consultant-led care", "timing": "Ongoing", "ref": "THH-BMI"},
                    {"text": "Dietician referral", "timing": "First trimester", "ref": "THH-BMI"},
                    {"text": "Anaesthetic review", "timing": "32 weeks", "ref": "THH-BMI"}
                ],
                "clarify": [
                    "Any other VTE risk factors (previous VTE, thrombophilia, immobility)?",
                    "Previous gestational diabetes?",
                    "Any difficulty with previous anaesthesia?",
                    "Any co-morbidities (OSA, hypertension, cardiac)?"
                ],
                "decisions": [
                    {"question": "Total VTE risk factors?", "options": ["4+ factors → LMWH from 1st trimester", "3 factors → LMWH from 28 weeks"]},
                    {"question": "OGTT result?", "options": ["Normal → routine care", "GDM → diabetes pathway"]}
                ],
                "plan": [
                    (16, "Obs ANC: counselling, dietician referral"),
                    (24, "OGTT 75g"),
                    (28, "Start LMWH if not already; assess VTE score"),
                    (32, "Anaesthetic counselling; growth scan"),
                    (36, "Growth scan; discuss postpartum VTE prophylaxis")
                ]
            })
        else:  # BMI 35-39.9
            guidelines.append({
                "name": "BMI 35-39.9 (Class II Obesity)",
                "code": "THH-BMI",
                "summary": f"BMI {bmi}. VTE/FGR risk assessment. OGTT 24-28w. Consider LMWH from 28w.",
                "actions": [
                    {"text": "Folic acid 5mg preconception", "ref": "THH-BMI", "default": False},
                    {"text": "VTE and FGR risk assessment at booking", "ref": "THH-BMI", "default": False},
                    {"text": "Vitamin D 25mcg or 1000IU", "ref": "THH-BMI", "default": False},
                    {"text": "Consider LMWH from 28w (+/- based on VTE score)", "ref": "THH-BMI", "default": False}
                ],
                "tests": [{"text": "OGTT 75g", "timing": "24-28 weeks", "ref": "NG3"}],
                "ultrasound": [{"text": "4-weekly growth scans", "timing": "From 32 weeks till birth", "ref": "THH-BMI"}],
                "followup": [
                    {"text": "Consultant-led care", "timing": "Ongoing", "ref": "THH-BMI"},
                    {"text": "Dietician referral (optional)", "timing": "First trimester", "ref": "THH-BMI"}
                ],
                "clarify": [
                    "Any other VTE risk factors?",
                    "Previous gestational diabetes?",
                    "Family history of diabetes?"
                ],
                "decisions": [
                    {"question": "VTE risk score ≥3?", "options": ["Yes → consider LMWH from 28w", "No → reassess postnatally"]}
                ],
                "plan": [
                    (16, "Obs ANC: counselling, consider dietician"),
                    (24, "OGTT 75g"),
                    (28, "Assess VTE score; consider LMWH"),
                    (32, "Obs ANC; growth scan"),
                    (36, "Obs ANC; growth scan; discuss postpartum VTE")
                ]
            })
    elif labs.get("BMI") and labs["BMI"] >= 30:
        guidelines.append({
            "name": "BMI 30-34.9 (Class I Obesity)",
            "code": "THH-BMI",
            "summary": f"BMI {labs['BMI']}. GDM screening required.",
            "tests": [{"text": "OGTT 75g", "timing": "24-28 weeks", "ref": "NG3"}],
            "plan": [(24, "OGTT")]
        })

    # GDM - THH gestational diabetes guideline
    if "gdm" in combined or "gestational diabetes" in combined:
        guidelines.append({
            "name": "Gestational Diabetes",
            "code": "THH-ANC",
            "summary": "GDM on diet: remote review 2-3 weekly, IOL 40+0-40+6. On treatment: 1-2 weekly review, IOL 39-40+0.",
            "actions": [
                {"text": "Joint diabetes clinic referral", "ref": "NG3", "default": False},
                {"text": "Home glucose monitoring", "ref": "NG3", "default": False}
            ],
            "tests": [
                {"text": "HbA1c if diagnosis in 1st/2nd trimester with RBS≥7", "timing": "At diagnosis", "ref": "THH-ANC"},
                {"text": "Home glucose monitoring 4x daily", "timing": "Ongoing", "ref": "NG3"}
            ],
            "ultrasound": [{"text": "4-weekly growth scans", "timing": "From 28 weeks (diet) or 28 weeks (treatment)", "ref": "THH-ANC"}],
            "followup": [
                {"text": "31-33w birth DSM preparation class", "timing": "31-33 weeks", "ref": "THH-ANC"},
                {"text": "36w Dr MOB and IOL discussion", "timing": "36 weeks", "ref": "THH-ANC"}
            ],
            "plan": [(28, "Growth scan"), (32, "Growth scan"), (36, "Growth scan + MOB discussion"), (39, "IOL if on treatment"), (40, "IOL if diet-controlled")]
        })

    # Previous Caesarean - GTG45, NG192, NG207, THH VBAC guideline
    if "caesarean" in combined or "c-section" in combined or "c section" in combined:
        guidelines.append({
            "name": "Previous Caesarean Section",
            "code": "GTG45",
            "summary": "VBAC vs ERCS counselling per GTG45/NG192. VBAC success 72-75% for 1 previous CS. Birth options clinic at 16w. Mode of birth at 36w.",
            "actions": [
                {"text": "Provide RCOG birth after CS leaflet at booking (GTG45)", "ref": "GTG45", "default": False},
                {"text": "Discuss VBAC success rates: 72-75% for 1 previous CS (GTG45)", "ref": "GTG45", "default": False},
                {"text": "Review indication for previous CS - spontaneous labour onset is favourable (GTG45)", "ref": "GTG45", "default": False},
                {"text": "Document informed decision about mode of birth (NG192)", "ref": "NG192", "default": False}
            ],
            "tests": [
                {"text": "Review previous CS operative notes if available", "timing": "Booking", "ref": "GTG45"}
            ],
            "followup": [
                {"text": "Birth options clinic with Senior MW (if 1 uncomplicated CS)", "timing": "16 weeks", "ref": "THH-VBAC"},
                {"text": "16w ANC with obstetrician (if 2+ uterine surgeries or complex)", "timing": "16 weeks", "ref": "GTG45"},
                {"text": "36w Obstetrician ANC - Mode of Birth decision", "timing": "36 weeks", "ref": "NG192"},
                {"text": "If VBAC planned, continuous CTG in labour (GTG45)", "timing": "Labour", "ref": "GTG45"}
            ],
            "clarify": [
                "Was previous CS in labour or prelabour (elective)?",
                "What was the indication for previous CS?",
                "Has she had a previous vaginal birth (increases VBAC success)?",
                "Inter-delivery interval >18 months (reduces uterine rupture risk)?"
            ],
            "decisions": [
                {"question": "Number of previous CS?", "options": ["1 uncomplicated → VBAC reasonable (GTG45)", "2+ → discuss with consultant, higher rupture risk"]},
                {"question": "Previous vaginal birth?", "options": ["Yes → higher VBAC success (87-90%)", "No → standard VBAC success (72-75%)"]},
                {"question": "If IOL considered (NG207)?", "options": ["Mechanical methods preferred for VBAC", "Avoid prostaglandins if possible (increased rupture risk)"]}
            ],
            "plan": [
                (16, "Birth options clinic / Obs ANC - provide information"),
                (36, "Mode of Birth discussion and documentation (NG192)"),
                (39, "If VBAC, offer IOL from 39w per NG207 if appropriate"),
                (41, "Do not exceed 41+0 for planned VBAC (GTG45)")
            ]
        })

    # Advanced Maternal Age >40
    if age and age >= 40:
        guidelines.append({
            "name": "Advanced Maternal Age (>40)",
            "code": "THH-ANC",
            "summary": "Aspirin risk assessment at 12w. Obs ANC at 16, 32, 36w. Offer IOL from 39w.",
            "actions": [
                {"text": "Aspirin risk assessment at 12 weeks", "ref": "THH-ANC", "default": False}
            ],
            "tests": [{"text": "28w one-off SFH measurement", "timing": "28 weeks", "ref": "THH-ANC"}],
            "ultrasound": [{"text": "4-weekly growth scans", "timing": "From 32 weeks till birth", "ref": "THH-ANC"}],
            "followup": [
                {"text": "16w Obstetrician ANC", "timing": "16 weeks", "ref": "THH-ANC"},
                {"text": "32 & 36w Obstetrician ANC", "timing": "32, 36 weeks", "ref": "THH-ANC"},
                {"text": "Offer IOL from 39 weeks", "timing": "39 weeks", "ref": "THH-ANC"}
            ],
            "plan": [(12, "Aspirin assessment"), (16, "Obs ANC"), (28, "SFH check"), (32, "Obs ANC + growth scan"), (36, "Obs ANC + growth scan"), (39, "Offer IOL")]
        })

    # Previous Preterm Labour - Preterm birth clinic pathway
    if "preterm" in combined or "premature" in combined:
        guidelines.append({
            "name": "Previous Preterm Labour",
            "code": "THH-PTB",
            "summary": "Refer to Preterm Birth Clinic. Cervical length scans. Consider progesterone if cervix <25mm.",
            "actions": [
                {"text": "Progesterone PV 400mg OD if cervical length <25mm (till 34w)", "ref": "THH-ANC", "default": False}
            ],
            "ultrasound": [
                {"text": "Cervical length scans", "timing": "16-24 weeks", "ref": "THH-PTB"},
                {"text": "Growth scans 4-weekly", "timing": "From 28 weeks", "ref": "THH-ANC"}
            ],
            "followup": [
                {"text": "Preterm Birth (PTB) Clinic referral", "timing": "First trimester", "ref": "THH-PTB"},
                {"text": "Consider Fetal Medicine referral if cerclage needed", "timing": "If cervix <25mm", "ref": "THH-PTB"}
            ],
            "clarify": [
                "At what gestation was the previous preterm birth?",
                "Was it spontaneous labour or indicated (e.g., pre-eclampsia, FGR)?",
                "Was there PPROM?",
                "Any cervical surgery (LLETZ, cone biopsy)?",
                "Any uterine anomaly?"
            ],
            "decisions": [
                {"question": "Previous spontaneous PTB <34w?", "options": ["Yes → cervical length scans from 16w", "No (indicated PTB) → address underlying cause"]},
                {"question": "Cervical length <25mm?", "options": ["Yes → start progesterone, consider cerclage referral", "No → continue surveillance"]}
            ],
            "plan": [
                (12, "PTB Clinic referral"),
                (16, "Cervical length scan"),
                (20, "Cervical length scan"),
                (24, "Cervical length scan; if <25mm start progesterone"),
                (28, "Growth scan"),
                (32, "Growth scan"),
                (36, "Growth scan; delivery planning")
            ]
        })

    return guidelines

def get_leaflets_for_patient(leaflet_tags):
    """Get relevant patient leaflets based on conditions"""
    leaflets = []
    for tag in leaflet_tags:
        if tag in PATIENT_LEAFLETS:
            leaflets.extend(PATIENT_LEAFLETS[tag])
    # Always add general leaflets
    leaflets.extend(PATIENT_LEAFLETS["general"])
    # Remove duplicates
    seen = set()
    unique = []
    for l in leaflets:
        if l["title"] not in seen:
            seen.add(l["title"])
            unique.append(l)
    return unique

# ================================================================
# SIDEBAR - Demo Use Cases
# ================================================================
with st.sidebar:
    st.title("🏥 Demo")

    # Demo use case dropdown - prominent at top
    st.markdown("**Select a Use Case**")
    selected_case = st.selectbox(
        "Use Case",
        list(DEMO_USE_CASES.keys()),
        label_visibility="collapsed"
    )

    # Show selected scenario preview
    if selected_case != "Select a use case...":
        st.caption(f"*{DEMO_USE_CASES[selected_case]}*")

    # Analyze button - immediately visible
    col1, col2 = st.columns(2)
    if col1.button("**Analyze**", type="primary", use_container_width=True):
        if selected_case != "Select a use case...":
            final_scenario = DEMO_USE_CASES[selected_case]
            st.session_state.scenario_text = final_scenario
            st.session_state.patient_data = parse_scenario(final_scenario)
            st.session_state.guidelines = get_applicable_guidelines(
                st.session_state.patient_data,
                final_scenario
            )
            st.session_state.analyzed = True
            st.session_state.history.append({"ts": datetime.now().isoformat(), "q": final_scenario[:50]})
            save_json(HISTORY_FILE, st.session_state.history[-50:])

    if col2.button("Clear", use_container_width=True):
        st.session_state.analyzed = False
        st.session_state.scenario_text = ""
        st.session_state.patient_data = None
        st.session_state.guidelines = []
        st.rerun()

    st.divider()

    # Optional: Custom scenario (collapsed by default)
    with st.expander("⚙️ Custom Scenario", expanded=False):
        # Gestation quick select with visual feedback
        st.markdown("**Gestation**")
        g_cols = st.columns(4)
        for col, wks in zip(g_cols, [16, 24, 28, 36]):
            is_selected = st.session_state.custom_weeks == wks
            button_label = f"✓ {wks}w" if is_selected else f"{wks}w"
            button_type = "primary" if is_selected else "secondary"
            if col.button(button_label, key=f"w{wks}", use_container_width=True, type=button_type):
                st.session_state.custom_weeks = wks
                st.rerun()

        # Conditions
        st.markdown("**Conditions**")
        conditions = ["Previous SGA", "Anaemia", "Previous Pre-eclampsia", "Twins"]
        cols = st.columns(2)
        for i, cond in enumerate(conditions):
            is_checked = cols[i % 2].checkbox(cond, key=f"cond_{cond}")
            if is_checked and cond not in st.session_state.custom_conditions:
                st.session_state.custom_conditions.append(cond)
            elif not is_checked and cond in st.session_state.custom_conditions:
                st.session_state.custom_conditions.remove(cond)

        # Text input with audio
        st.markdown("**Describe scenario**")
        input_cols = st.columns([0.85, 0.15])

        # Audio recording button
        with input_cols[1]:
            audio = st.audio_input("Record", label_visibility="collapsed", key=f"audio_{st.session_state.audio_counter}")

        # Process audio if recorded
        if audio:
            with st.spinner("Transcribing..."):
                transcription = transcribe_audio(audio)
                if transcription and not transcription.startswith("⚠️"):
                    existing = st.session_state.custom_free_text
                    if existing and not existing.endswith(" "):
                        st.session_state.custom_free_text = existing + " " + transcription
                    else:
                        st.session_state.custom_free_text = (existing + transcription) if existing else transcription
                    st.session_state.audio_counter += 1
                    st.rerun()
                else:
                    st.error(transcription or "Transcription failed")

        # Text area
        with input_cols[0]:
            free_text = st.text_area(
                "Scenario",
                height=80,
                placeholder="e.g., 32yo G2P1, previous C-section, BMI 35, on aspirin...",
                label_visibility="collapsed",
                value=st.session_state.custom_free_text
            )
            st.session_state.custom_free_text = free_text

        # Build custom scenario from all sources
        custom_parts = []
        if st.session_state.custom_weeks:
            custom_parts.append(f"{st.session_state.custom_weeks} weeks")
        if st.session_state.custom_conditions:
            custom_parts.append(", ".join(st.session_state.custom_conditions))
        if free_text:
            custom_parts.append(free_text)
        custom_scenario = ", ".join(custom_parts) if custom_parts else ""

        # Show preview of combined scenario
        if custom_scenario:
            st.caption(f"**Combined query:** {custom_scenario}")

        # Analyze button - always show but only enabled if there's content
        analyze_col, clear_col = st.columns(2)
        if analyze_col.button("Analyze Custom", type="primary", use_container_width=True, disabled=not custom_scenario):
            st.session_state.scenario_text = custom_scenario
            st.session_state.patient_data = parse_scenario(custom_scenario)
            st.session_state.guidelines = get_applicable_guidelines(
                st.session_state.patient_data,
                custom_scenario
            )
            st.session_state.analyzed = True
            st.session_state.history.append({"ts": datetime.now().isoformat(), "q": custom_scenario[:50]})
            save_json(HISTORY_FILE, st.session_state.history[-50:])
            st.rerun()

        if clear_col.button("Clear Custom", use_container_width=True):
            st.session_state.custom_weeks = None
            st.session_state.custom_conditions = []
            st.session_state.custom_free_text = ""
            st.rerun()

# ================================================================
# MAIN PANEL
# ================================================================

# Header - compact design
st.markdown("""
<div style='margin: 0; padding: 0;'>
    <h3 style='margin: 0 0 2px 0; padding: 0; font-size: 32px; font-weight: bold;'>GuidelinesIQ:Maternity</h3>
    <p style='margin: 0 0 5px 0; padding: 0; font-size: 18px; color: #666;'>Clinical decision support for safer care</p>
    <hr style='margin: 0; padding: 0; height: 1px; border: none; background-color: #ddd;'>
</div>
""", unsafe_allow_html=True)

if not st.session_state.analyzed:
    # Welcome message
    st.markdown("## Summary")
    st.info("""
**Welcome to GuidelinesIQ:Maternity**

Clinical decision support for safer antenatal care.

**How to use:**
1. Select a demo use case or build a custom scenario from the left panel
2. Or enter a free-text clinical scenario (with voice input support)
3. Click **Analyze** to generate evidence-based recommendations

**Features:**
- ✅ Evidence-based guidelines (NICE, RCOG, Hillingdon protocols)
- ✅ Transparent recommendations with source references
- ✅ Customizable - select/deselect relevant guidelines
- ✅ Tests, ultrasound, and follow-up checklists
- ✅ Patient-friendly care summaries for shared decision-making
- ✅ Timeline-based care planning

*Select a scenario on the left to begin.*
    """)

else:
    # Show results with tabs
    patient_data = st.session_state.patient_data
    guidelines = st.session_state.guidelines
    weeks = patient_data.get("weeks") or 20  # Default to 20 if None or not specified

    # Collect all items from guidelines (before tabs so both can access)
    all_tests = []
    all_ultrasound = []
    all_followup = []
    all_plan = []
    all_clarify = []
    all_decisions = []

    for g in guidelines:
        all_tests.extend(g.get("tests", []))
        all_ultrasound.extend(g.get("ultrasound", []))
        # Filter follow-ups to only include those at or after current gestational age
        for fu in g.get("followup", []):
            fu_weeks = extract_weeks_from_timing(fu['timing'])
            # Include if: no specific week, or if specific week is >= current weeks
            if fu_weeks is None or fu_weeks >= weeks:
                all_followup.append(fu)
        all_clarify.extend(g.get("clarify", []))
        all_decisions.extend(g.get("decisions", []))
        if g.get("plan"):
            all_plan.extend([(w, d) for w, d in g["plan"] if w >= weeks])

    # Deduplicate tests by text
    seen_tests = set()
    unique_tests = []
    for t in all_tests:
        if t['text'] not in seen_tests:
            seen_tests.add(t['text'])
            unique_tests.append(t)
    all_tests = unique_tests

    # Deduplicate ultrasound by text
    seen_us = set()
    unique_us = []
    for u in all_ultrasound:
        if u['text'] not in seen_us:
            seen_us.add(u['text'])
            unique_us.append(u)
    all_ultrasound = unique_us

    # Merge duplicate follow-up items
    merged_followup = {}
    for f in all_followup:
        key = f['text']
        if key not in merged_followup:
            merged_followup[key] = {"text": f['text'], "timing": f['timing'], "refs": []}
        if f['ref'] not in merged_followup[key]["refs"]:
            merged_followup[key]["refs"].append(f['ref'])
    all_followup_merged = list(merged_followup.values())

    # Deduplicate clarify questions
    all_clarify = list(dict.fromkeys(all_clarify))

    # Deduplicate and clean risk factors
    risks = patient_data.get("risks", [])
    if patient_data.get("bmi"):
        risks = [r for r in risks if not r.startswith("BMI")]
    unique_risks = list(dict.fromkeys(risks))

    # Collect selected actions from checkboxes (for both tabs to use)
    selected_actions_list = []
    selected_tests_list = []
    for g in guidelines:
        for idx, action in enumerate(g.get("actions", [])):
            key = f"act_{g['code']}_{g['name'][:5]}_{idx}"
            if key in st.session_state and st.session_state[key]:
                selected_actions_list.append(action['text'])
    for i, t in enumerate(all_tests):
        key = f"test_{t['text'][:20]}_{i}"
        if key in st.session_state and st.session_state[key]:
            selected_tests_list.append(t['text'])

    # TABS
    tab_clinical, tab_patient = st.tabs(["📋 Clinical Care", "👤 Patient-led Care"])

    # ================================================================
    # TAB 1: CLINICAL CARE
    # ================================================================
    with tab_clinical:

        # SUMMARY
        st.markdown("## Summary")

        # Build compact summary
        summary_parts = []
        if patient_data.get("age"):
            summary_parts.append(f"**{patient_data['age']}yo**")
        if patient_data.get("parity"):
            summary_parts.append(patient_data["parity"])
        if patient_data.get("weeks"):
            summary_parts.append(f"**{patient_data['weeks']}w**")
        if patient_data.get("bmi"):
            bmi = patient_data['bmi']
            if bmi >= 40:
                summary_parts.append(f"BMI {bmi} (Class III)")
            elif bmi >= 35:
                summary_parts.append(f"BMI {bmi} (Class II)")
            elif bmi >= 30:
                summary_parts.append(f"BMI {bmi}")

        # Build summary info box
        summary_text = " · ".join(summary_parts) if summary_parts else ""
        if unique_risks:
            summary_text += f"\n\n**Risks:** {', '.join(unique_risks)}"

        # Add applicable guidelines
        if guidelines:
            guideline_names = [g['name'] for g in guidelines]
            summary_text += f"\n\n**Guidelines:** {', '.join(guideline_names)}"

        st.info(summary_text if summary_text else "Enter scenario details to generate recommendations.")

        # GUIDELINES
        st.markdown("## Guidelines")
        st.caption("*Expand to see actions. Selected actions will appear in summary.*")

        if guidelines:
            for g in guidelines:
                with st.expander(f"📁 {g['name']}", expanded=False):
                    st.caption(f"*{g['summary']}*")
                    st.divider()
                    for idx, action in enumerate(g.get("actions", [])):
                        key = f"act_{g['code']}_{g['name'][:5]}_{idx}"
                        st.checkbox(
                            f"{action['text']} {make_link(action['ref'])}",
                            value=action.get("default", False),
                            key=key
                        )
        else:
            st.caption("No specific guidelines triggered. Add more details.")

        # 🧪 TESTS (Checkboxes)
        st.markdown("## 🧪 Tests")
        if all_tests:
            for i, t in enumerate(all_tests):
                key = f"test_{t['text'][:20]}_{i}"
                st.checkbox(
                    f"**{t['text']}** — *{t['timing']}* {make_link(t['ref'])}",
                    key=key,
                    value=False
                )
        else:
            st.caption("Routine bloods as per gestation")

        # 🔬 ULTRASOUND
        st.markdown("## 🔬 Ultrasound")
        if all_ultrasound:
            for s in all_ultrasound:
                st.markdown(f"• **{s['text']}** — *{s['timing']}* {make_link(s['ref'])}")
        else:
            st.caption("Routine scans as per gestation")

        # 📅 FOLLOW UP (Referrals & Specialist Care)
        st.markdown("## 📅 Follow Up")
        st.caption("*Referrals and specialist involvement:*")
        if all_followup_merged:
            for item in all_followup_merged:
                if len(item["refs"]) == 1:
                    st.markdown(f"• **{item['text']}** — *{item['timing']}* {make_link(item['refs'][0])}")
                else:
                    refs_str = ", ".join([make_link(r) for r in item["refs"]])
                    st.markdown(f"• **{item['text']}** — *{item['timing']}* ({refs_str})")
        else:
            st.caption("Routine midwifery-led care")

        if all_clarify:
            st.markdown("## ❓ Clarify")
            st.caption("*Questions to ask the patient to individualise care:*")
            for q in all_clarify:
                st.markdown(f"• {q}")

        # 🔀 DECISION POINTS (Collapsible)
        if all_decisions:
            with st.expander("🔀 **Decision Points**", expanded=False):
                st.caption("*Clinical decision trees based on patient responses:*")
                for d in all_decisions:
                    st.markdown(f"**{d['question']}**")
                    for opt in d['options']:
                        st.markdown(f"  → {opt}")
                    st.markdown("")

        # 📆 PLAN & MANAGEMENT (Collapsible)
        with st.expander("📆 **Plan & Management**", expanded=False):
            st.caption("*Timeline of investigations, scans, and key actions:*")
            if all_plan:
                all_plan_sorted = sorted(set(all_plan), key=lambda x: x[0])
                for target_week, desc in all_plan_sorted[:12]:
                    weeks_away = target_week - weeks
                    if weeks_away <= 0:
                        st.markdown(f"• **Now:** {desc}")
                    elif target_week > 40:
                        st.markdown(f"• **Postnatal:** {desc}")
                    else:
                        st.markdown(f"• **{target_week}w** (in {weeks_away}w): {desc}")
            else:
                st.caption("Routine antenatal schedule")

        # ✅ SELECTED ACTIONS (Dynamic summary of clicked items)
        if selected_actions_list or selected_tests_list:
            st.markdown("## ✅ Selected Actions")
            st.caption("*Items you've selected from guidelines and tests:*")
            if selected_actions_list:
                for action in selected_actions_list:
                    st.markdown(f"• {action}")
            if selected_tests_list:
                for test in selected_tests_list:
                    st.markdown(f"• 🧪 {test}")

        # 📋 COPY SUMMARY (Collapsible)
        with st.expander("📋 **Copy Summary**", expanded=False):
            # Build merged follow-up texts
            merged_fu_texts = []
            for item in all_followup_merged:
                if len(item["refs"]) == 1:
                    merged_fu_texts.append(f"{item['text']} [{item['refs'][0]}]")
                else:
                    merged_fu_texts.append(f"{item['text']} [{', '.join(item['refs'])}]")

            # Include selected actions and tests
            selected_items = selected_actions_list + [f"TEST: {t}" for t in selected_tests_list]

            txt = f"""SUMMARY | {datetime.now().strftime('%d/%m/%Y')}
{weeks}w | {patient_data.get('parity', '-')} | Age {patient_data.get('age', '?')}
Risks: {', '.join(unique_risks) or 'None'}
Guidelines: {', '.join([g['name'] for g in guidelines]) or 'None'}

SELECTED ACTIONS: {'; '.join(selected_items) or 'None selected'}
TESTS: {'; '.join([t['text'] for t in all_tests]) or 'Routine'}
ULTRASOUND: {'; '.join([s['text'] for s in all_ultrasound]) or 'Routine'}
FOLLOW UP: {'; '.join(merged_fu_texts) or 'Routine'}
"""
            # Initialize session state for clinical summary
            if "clinical_summary_text" not in st.session_state or st.session_state.get("clinical_summary_base") != txt:
                st.session_state.clinical_summary_text = txt
                st.session_state.clinical_summary_base = txt
            if "clinical_summary_edit_mode" not in st.session_state:
                st.session_state.clinical_summary_edit_mode = False

            # Show read-only or editable based on mode
            if st.session_state.clinical_summary_edit_mode:
                st.session_state.clinical_summary_text = st.text_area(
                    "Edit summary:",
                    value=st.session_state.clinical_summary_text,
                    height=250,
                    key="clinical_summary_editor",
                    label_visibility="collapsed"
                )
                st.markdown('<div class="small-edit-btn">', unsafe_allow_html=True)
                if st.button("✓ Done", key="clinical_done_btn"):
                    st.session_state.clinical_summary_edit_mode = False
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.code(st.session_state.clinical_summary_text, language=None)
                st.markdown('<div class="small-edit-btn">', unsafe_allow_html=True)
                if st.button("✎ Edit", key="clinical_edit_btn"):
                    st.session_state.clinical_summary_edit_mode = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.caption("⚠️ Decision support only. Verify against current guidelines.")

    # ================================================================
    # TAB 2: PATIENT-LED CARE
    # ================================================================
    with tab_patient:
        st.markdown("## 👤 Patient-led Care")
        st.markdown("*Resources and leaflets to share with the patient for informed decision-making.*")

        # Patient-friendly summary
        st.markdown("### 📝 Your Care Summary")

        # Build patient-friendly text
        patient_summary = []

        # Basic info in lay terms
        if patient_data.get("weeks"):
            patient_summary.append(f"You are currently **{patient_data['weeks']} weeks pregnant**.")

        # Explain risk factors in lay terms
        risks = patient_data.get("risks", [])
        if risks:
            patient_summary.append("\n**What we're monitoring:**")
            for risk in risks:
                risk_lower = risk.lower()
                if "epilepsy" in risk_lower:
                    patient_summary.append("• Your epilepsy - we'll work with specialists to keep you and baby safe while managing your medication")
                elif "bmi" in risk_lower or "obesity" in risk_lower:
                    patient_summary.append("• Your weight - we'll offer extra support including blood sugar testing and additional scans")
                elif "sga" in risk_lower or "small" in risk_lower:
                    patient_summary.append("• Baby's growth - because of your history, we'll do extra scans to check baby is growing well")
                elif "dvt" in risk_lower or "vte" in risk_lower:
                    patient_summary.append("• Blood clot prevention - you'll need blood-thinning injections to keep you safe")
                elif "preterm" in risk_lower:
                    patient_summary.append("• Risk of early labour - we'll monitor your cervix and discuss ways to reduce this risk")
                elif "pre-eclampsia" in risk_lower:
                    patient_summary.append("• Blood pressure - we'll check this regularly and watch for warning signs")
                elif "caesarean" in risk_lower:
                    patient_summary.append("• Previous caesarean - we'll discuss your options for this birth")
                elif "diabetes" in risk_lower or "gdm" in risk_lower:
                    patient_summary.append("• Blood sugar levels - we'll help you monitor and manage these")
                else:
                    patient_summary.append(f"• {risk}")

        # What your care team has planned (selected actions in lay terms)
        if selected_actions_list:
            patient_summary.append("\n**Your care plan includes:**")
            for action in selected_actions_list:
                action_lower = action.lower()
                # Translate clinical actions to patient-friendly language
                if "aspirin" in action_lower:
                    patient_summary.append("• Daily low-dose aspirin to reduce risk of complications")
                elif "folic acid 5mg" in action_lower:
                    patient_summary.append("• High-dose folic acid (5mg daily) for healthy baby development")
                elif "vitamin d" in action_lower:
                    patient_summary.append("• Vitamin D supplement to support your and baby's health")
                elif "lmwh" in action_lower or "blood-thinning" in action_lower or "clexane" in action_lower:
                    patient_summary.append("• Daily injections to prevent blood clots")
                elif "dietician" in action_lower or "dietitian" in action_lower:
                    patient_summary.append("• Support from a dietitian for healthy eating in pregnancy")
                elif "anaesthetic" in action_lower:
                    patient_summary.append("• Meeting with an anaesthetist to discuss pain relief options for birth")
                elif "glucose monitoring" in action_lower or "blood sugar" in action_lower:
                    patient_summary.append("• Regular checks of your blood sugar levels")
                elif "iron" in action_lower and "oral" in action_lower:
                    patient_summary.append("• Iron tablets to treat anaemia")
                elif "ferinject" in action_lower:
                    patient_summary.append("• Iron infusion (intravenous) if tablets don't work")
                elif "ursodeoxycholic acid" in action_lower:
                    patient_summary.append("• Medication to help with itching and protect baby")
                elif "progesterone" in action_lower:
                    patient_summary.append("• Progesterone pessaries to reduce risk of early labour")
                elif "vbac" in action_lower or "birth after cs" in action_lower:
                    patient_summary.append("• Information leaflet about birth options after caesarean")
                elif "birth options" in action_lower or "mode of birth" in action_lower:
                    patient_summary.append("• Discussion about your birth options (vaginal birth or caesarean)")
                elif "vbac success" in action_lower:
                    patient_summary.append("• Good chance of vaginal birth (around 72-75% success rate)")
                elif "epilepsy register" in action_lower:
                    patient_summary.append("• Registration on pregnancy epilepsy register for research")
                elif "vte risk" in action_lower:
                    patient_summary.append("• Assessment of your blood clot risk")
                elif "fgr risk" in action_lower or "growth" in action_lower and "risk" in action_lower:
                    patient_summary.append("• Assessment of baby's growth risk factors")
                elif "saving babies" in action_lower or "sbl3" in action_lower:
                    patient_summary.append("• Following national guidelines for monitoring baby's growth")
                elif "grow chart" in action_lower or "customised" in action_lower:
                    patient_summary.append("• Personalised growth chart to track your baby's size")
                elif "thh fgr" in action_lower or "local fgr" in action_lower:
                    patient_summary.append("• Following local hospital guidelines for baby's growth monitoring")
                elif "previous cs" in action_lower or "operative notes" in action_lower:
                    patient_summary.append("• Review of your previous caesarean details")
                elif "ctg" in action_lower or "continuous monitoring" in action_lower:
                    patient_summary.append("• Continuous heart rate monitoring for baby during labour")
                elif "informed decision" in action_lower or "document" in action_lower and "decision" in action_lower:
                    patient_summary.append("• Your birth preferences will be documented")
                elif "cervical length" in action_lower:
                    patient_summary.append("• Scan to measure your cervix length")
                elif "drug level" in action_lower or "lamotrigine" in action_lower:
                    patient_summary.append("• Blood tests to check your medication levels")
                elif "fetal echo" in action_lower or "cardiac" in action_lower:
                    patient_summary.append("• Detailed heart scan for baby")
                elif "neurology" in action_lower:
                    patient_summary.append("• Appointment with neurologist for epilepsy care")
                else:
                    # If no match, show original but try to simplify
                    simplified = action.replace("ANC", "antenatal clinic")
                    simplified = simplified.replace("Obs Med", "obstetric medicine team")
                    simplified = simplified.replace("GTG31", "").replace("SBL3", "").replace("THH-FGR", "")
                    simplified = simplified.replace("NG192", "").replace("NG207", "").replace("GTG45", "")
                    simplified = simplified.strip(" -()").strip()
                    if simplified:
                        patient_summary.append(f"• {simplified}")

        # What tests have been selected
        if selected_tests_list:
            patient_summary.append("\n**Tests you'll need:**")
            for test in selected_tests_list[:3]:  # Show first 3
                test_lower = test.lower()
                if "ogtt" in test_lower or "glucose" in test_lower:
                    patient_summary.append("• Sugar drink test to check for diabetes")
                elif "doppler" in test_lower:
                    patient_summary.append("• Special ultrasound to check blood flow")
                elif "bile acids" in test_lower:
                    patient_summary.append("• Blood test for liver function")
                elif "thrombophilia" in test_lower:
                    patient_summary.append("• Blood test to check clotting")
                elif "drug levels" in test_lower:
                    patient_summary.append("• Blood test to check medication levels")
                else:
                    patient_summary.append(f"• {test}")

        # What scans to expect
        if all_ultrasound:
            patient_summary.append("\n**Scans you'll have:**")
            for scan in all_ultrasound[:3]:  # Show first 3
                patient_summary.append(f"• {scan['text']} ({scan['timing']})")

        # Who you'll see
        if all_followup_merged:
            patient_summary.append("\n**Who you'll see:**")
            for fu in all_followup_merged[:3]:  # Show first 3
                patient_summary.append(f"• {fu['text']}")

        # Display patient summary with edit toggle
        if patient_summary:
            patient_summary_txt = "\n".join(patient_summary)
            # Initialize session state for patient summary
            if "patient_summary_text" not in st.session_state or st.session_state.get("patient_summary_base") != patient_summary_txt:
                st.session_state.patient_summary_text = patient_summary_txt
                st.session_state.patient_summary_base = patient_summary_txt
            if "patient_summary_edit_mode" not in st.session_state:
                st.session_state.patient_summary_edit_mode = False

            # Show read-only or editable based on mode
            st.caption("*A simple explanation of your care plan:*")
            if st.session_state.patient_summary_edit_mode:
                st.session_state.patient_summary_text = st.text_area(
                    "Edit patient summary:",
                    value=st.session_state.patient_summary_text,
                    height=300,
                    key="patient_summary_editor",
                    label_visibility="collapsed"
                )
                st.markdown('<div class="small-edit-btn">', unsafe_allow_html=True)
                if st.button("✓ Done", key="patient_done_btn"):
                    st.session_state.patient_summary_edit_mode = False
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info(st.session_state.patient_summary_text)
                st.markdown('<div class="small-edit-btn">', unsafe_allow_html=True)
                if st.button("✎ Edit", key="patient_edit_btn"):
                    st.session_state.patient_summary_edit_mode = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Your care plan will appear here once your details are entered.")

        st.divider()

        # Get relevant leaflets
        leaflet_tags = patient_data.get("leaflet_tags", [])
        leaflets = get_leaflets_for_patient(leaflet_tags)

        st.markdown("### 📚 Patient Information Leaflets")
        st.caption("*Select leaflets to share with the patient:*")

        if leaflets:
            # Group by source
            nice_leaflets = [l for l in leaflets if l["source"] == "NICE"]
            rcog_leaflets = [l for l in leaflets if l["source"] == "RCOG"]
            hillingdon_leaflets = [l for l in leaflets if l["source"] == "Hillingdon"]
            other_leaflets = [l for l in leaflets if l["source"] not in ["NICE", "RCOG", "Hillingdon"]]

            if nice_leaflets:
                st.markdown("#### NICE Patient Information")
                for l in nice_leaflets:
                    col1, col2 = st.columns([0.05, 0.95])
                    col1.checkbox("Select", key=f"leaf_nice_{l['title'][:20]}", label_visibility="collapsed")
                    col2.markdown(f"[{l['title']}]({l['url']})")

            if rcog_leaflets:
                st.markdown("#### RCOG Patient Information")
                for l in rcog_leaflets:
                    col1, col2 = st.columns([0.05, 0.95])
                    col1.checkbox("Select", key=f"leaf_rcog_{l['title'][:20]}", label_visibility="collapsed")
                    col2.markdown(f"[{l['title']}]({l['url']})")

            if hillingdon_leaflets:
                st.markdown("#### Hillingdon Hospital Leaflets")
                for l in hillingdon_leaflets:
                    col1, col2 = st.columns([0.05, 0.95])
                    col1.checkbox("Select", key=f"leaf_hil_{l['title'][:20]}", label_visibility="collapsed")
                    col2.markdown(f"[{l['title']}]({l['url']})")

            if other_leaflets:
                st.markdown("#### Other Resources")
                for l in other_leaflets:
                    col1, col2 = st.columns([0.05, 0.95])
                    col1.checkbox("Select", key=f"leaf_other_{l['title'][:20]}", label_visibility="collapsed")
                    col2.markdown(f"[{l['title']}]({l['url']}) — *{l['source']}*")

            st.divider()

            # Action buttons
            col1, col2 = st.columns(2)
            col1.button("📧 Email selected to patient", use_container_width=True)
            col2.button("🖨️ Print selected leaflets", use_container_width=True)

        else:
            st.info("No specific leaflets identified. General antenatal information available above.")

        st.divider()

        st.markdown("### 💬 Discussion Points")
        st.caption("*Key topics to discuss with the patient:*")

        discussion_points = []
        risks = patient_data.get("risks", [])

        if any("pre-eclampsia" in r.lower() for r in risks):
            discussion_points.append("Warning signs of pre-eclampsia (headache, visual disturbance, epigastric pain)")
        if any("gdm" in r.lower() or "diabetes" in r.lower() for r in risks):
            discussion_points.append("Blood glucose targets and monitoring schedule")
            discussion_points.append("Dietary advice and lifestyle modifications")
        if any("anaemia" in r.lower() for r in risks):
            discussion_points.append("Iron supplementation - how to take, side effects")
        if any("twins" in r.lower() for r in risks):
            discussion_points.append("Signs of preterm labour")
            discussion_points.append("Delivery planning and options")
        if any("cholestasis" in r.lower() for r in risks):
            discussion_points.append("Importance of reporting worsening itch")
            discussion_points.append("Stillbirth risk and monitoring plan")
        if any("vte" in r.lower() for r in risks):
            discussion_points.append("How to inject LMWH")
            discussion_points.append("Signs of DVT/PE to watch for")
        if any("epilepsy" in r.lower() for r in risks):
            discussion_points.append("Importance of medication adherence")
            discussion_points.append("Safety advice (bathing, heights)")

        # Default points
        discussion_points.append("Fetal movements - what's normal, when to seek help")
        discussion_points.append("Next appointment and what to expect")

        for point in discussion_points:
            st.checkbox(point, key=f"discuss_{point[:20]}")
