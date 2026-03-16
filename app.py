"""
Clinical Decision Support System
"""

import streamlit as st
import json
import os
from datetime import datetime
import re

st.set_page_config(page_title="Clinical Decision Support", page_icon="🏥", layout="wide")

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

# Demo use cases
DEMO_USE_CASES = {
    "Select a use case...": "",
    "Use Case 1: Epilepsy + Lamotrigine": "24 year old with a history of epilepsy, last seizure 4 months ago, on lamotrigine, currently 16 weeks pregnant",
    "Use Case 2: High BMI + Previous SGA": "40 year old, BMI of 35 with a history of Caesarean section at 34 weeks for small baby 3 years ago, currently 28 weeks pregnant",
    "Use Case 3: Previous Preterm": "29 year old, previous preterm labour at 30 weeks",
    "Use Case 4: High BMI + DVT": "42 year old, BMI of 45, Para 2 and previous history of DVT",
}

# Patient leaflets database
PATIENT_LEAFLETS = {
    "pre-eclampsia": [
        {"title": "Pre-eclampsia: what you need to know", "source": "NICE", "url": "https://www.nice.org.uk/guidance/ng133/ifp/chapter/pre-eclampsia"},
        {"title": "Pre-eclampsia patient information", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/pre-eclampsia-patient-information-leaflet/"},
        {"title": "High blood pressure in pregnancy", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "gestational_diabetes": [
        {"title": "Gestational diabetes: what you need to know", "source": "NICE", "url": "https://www.nice.org.uk/guidance/ng3/ifp/chapter/gestational-diabetes"},
        {"title": "Gestational diabetes patient information", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/gestational-diabetes-patient-information-leaflet/"},
        {"title": "Diabetes in pregnancy", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "anaemia": [
        {"title": "Anaemia in pregnancy", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/"},
        {"title": "Iron supplements in pregnancy", "source": "NHS", "url": "https://www.nhs.uk/pregnancy/keeping-well/vitamins-supplements-and-nutrition/"},
        {"title": "Eating well in pregnancy", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "twins": [
        {"title": "Multiple pregnancy: having more than one baby", "source": "NICE", "url": "https://www.nice.org.uk/guidance/ng137/ifp/chapter/about-this-information"},
        {"title": "Multiple pregnancy patient information", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/multiple-pregnancy-patient-information-leaflet/"},
        {"title": "Twin pregnancy information", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "sga": [
        {"title": "Small for gestational age baby", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/small-for-gestational-age-baby-patient-information-leaflet/"},
        {"title": "Your baby's growth", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "cholestasis": [
        {"title": "Obstetric cholestasis patient information", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/obstetric-cholestasis-patient-information-leaflet/"},
        {"title": "Itching in pregnancy (ICP)", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "thrombocytopenia": [
        {"title": "Low platelet count in pregnancy", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/"},
        {"title": "Blood conditions in pregnancy", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "vte": [
        {"title": "Reducing the risk of blood clots", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/reducing-the-risk-of-venous-thromboembolism-during-pregnancy-and-after-birth-patient-information-leaflet/"},
        {"title": "Blood clots in pregnancy", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "epilepsy": [
        {"title": "Epilepsy and pregnancy", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/epilepsy-in-pregnancy-patient-information-leaflet/"},
        {"title": "Epilepsy UK pregnancy guide", "source": "Epilepsy Action", "url": "https://www.epilepsy.org.uk/info/women/pregnancy"},
    ],
    "breech": [
        {"title": "Turning a breech baby (ECV)", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/turning-a-breech-baby-in-the-womb-external-cephalic-version-patient-information-leaflet/"},
        {"title": "Breech baby: your options", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/documents/_Patients/PatientLeaflets/maternity/"},
    ],
    "reduced_movements": [
        {"title": "Your baby's movements", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/your-babys-movements-in-pregnancy-patient-information-leaflet/"},
        {"title": "Reduced fetal movements", "source": "Kicks Count", "url": "https://www.kickscount.org.uk/"},
    ],
    "general": [
        {"title": "Antenatal care: your options", "source": "NICE", "url": "https://www.nice.org.uk/guidance/ng201/ifp/chapter/about-this-information"},
        {"title": "Pregnancy and birth", "source": "RCOG", "url": "https://www.rcog.org.uk/for-the-public/browse-all-patient-information-leaflets/"},
        {"title": "Antenatal appointments", "source": "Hillingdon", "url": "https://www.thh.nhs.uk/services/maternity/antenatal-care/"},
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
    # National Guidelines - RCOG Green-top (public links)
    "GTG68": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/epilepsy-in-pregnancy-green-top-guideline-no-68/",
    "GTG37a": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/reducing-the-risk-of-thrombosis-and-embolism-during-pregnancy-and-the-puerperium-green-top-guideline-no-37a/",
    "GTG37b": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/thrombosis-and-embolism-during-pregnancy-and-the-puerperium-acute-management-green-top-guideline-no-37b/",
    "GTG72": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/care-of-women-with-obesity-in-pregnancy-green-top-guideline-no-72/",
    "GTG31": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/small-for-gestational-age-fetus-green-top-guideline-no-31/",
    "GTG43": "https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/obstetric-cholestasis-green-top-guideline-no-43/",
    # Local Guidelines (Hillingdon/THH) - Direct links from Antenatal Care Schedule
    "THH-Epilepsy": SHAREPOINT_BASE + "202405211452040.Epilepsy%20in%20pregnancy%20V7.pdf",
    "THH-FGR": SHAREPOINT_BASE + "202411210723400.FGR%20Guideline%202024%20Hillingdon%202024.pdf",
    "THH-BMI": SHAREPOINT_FOLDER,  # "Raised Body Mass Index (BMI) in pregnancy guideline" - no specific PDF found
    "THH-VBAC": SHAREPOINT_BASE + "202506241450060.Vaginal%20birth%20after%20csection%20VBAC%20V7.0.pdf",
    "THH-VTE": SHAREPOINT_FOLDER,  # VTE Prophylaxis flowchart in Antenatal Care Schedule
    "THH-PTB": SHAREPOINT_FOLDER,  # Preterm Birth Clinic Pathway
    "THH-ANC": SHAREPOINT_BASE + "202512191144050.Maternal%20Antenatal%20screening%20tests%20Guidelines%20v5.1.pdf",
    "THH-Anaemia": SHAREPOINT_BASE + "202511211517060.Anaemia%20and%20Ferinject%20Infusion%20in%20Pregnancy%20v3.1.pdf",
    "THH-GDM": SHAREPOINT_BASE + "202512191131340.gestational%20diabetes%20guideline%20v4.1.pdf",
    "THH-Hypertension": SHAREPOINT_BASE + "202601301510290.Antenatal%20Hypertension%20Pregnancy%20V5.1.pdf",
    "THH-Thyroid": SHAREPOINT_BASE + "202504141031280.Thyroid%20guideline%20V3.0.pdf",
    # Additional local guidelines from Antenatal Care Schedule
    "THH-Antibodies": SHAREPOINT_BASE + "202502241020400.Antibodies%20in%20pregnancy%20V5.0.pdf",
    "THH-SickleCell": SHAREPOINT_BASE + "202601231300520.Sickle%20Cell%20Disease%20and%20Pregnancy%20v5.0.pdf",
    "THH-Syphilis": SHAREPOINT_BASE + "202212011531480.Management%20of%20Positive%20Syphilis%20Serology%20in%20Pregnancy%20v.4.0.pdf",
    "THH-ChickenPox": SHAREPOINT_BASE + "202204111056350.Chicken%20pox%20in%20pregnancy.pdf",
    "THH-Herpes": SHAREPOINT_BASE + "202411110820540.Genital%20warts%20in%20pregnancy%20V5.0.pdf",
    "THH-LGA": SHAREPOINT_BASE + "202405211458230.Management%20of%20large%20for%20gestational%20age%20foetuses%20and%20macrosomia%20V2.0.pdf",
    "THH-Ultrasound": SHAREPOINT_BASE + "202507081315310.Obstetric_ultrasound%20protocol%20V4.0.pdf",
    "THH-MEWS": SHAREPOINT_BASE + "202506241703290.MEWS%20Early%20recognition%20of%20the%20severely%20ill%20pregnant%20woman%20V3.0.pdf",
}

def make_link(ref):
    code = ref.split()[0] if ref else ""
    for key, url in GUIDELINE_URLS.items():
        if key in code:
            return f"[{ref}]({url})"
    return ref

def parse_scenario(text):
    """Parse free text scenario into structured data"""
    text_lower = text.lower()
    data = {"age": None, "weeks": None, "parity": None, "bmi": None, "risks": [], "labs": {}, "leaflet_tags": []}

    # Age
    age_match = re.search(r'(\d+)\s*(?:year|yr|y/?o)', text_lower)
    if age_match:
        data["age"] = int(age_match.group(1))

    # Weeks
    weeks_match = re.search(r'(\d+)\s*weeks?', text_lower)
    if weeks_match:
        data["weeks"] = int(weeks_match.group(1))

    # BMI
    bmi_match = re.search(r'bmi\s*(?:of\s*)?(\d+(?:\.\d+)?)', text_lower)
    if bmi_match:
        data["bmi"] = float(bmi_match.group(1))
        data["labs"]["BMI"] = data["bmi"]
        if data["bmi"] >= 30:
            data["risks"].append(f"BMI {data['bmi']}")

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
        ("caesarean", "Previous Caesarean", None), ("c-section", "Previous Caesarean", None),
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

    return data

def get_applicable_guidelines(patient_data, risks_text):
    """Get guidelines based on conditions - aligned with THH Antenatal Care Schedule"""
    guidelines = []
    combined = risks_text.lower()
    labs = patient_data.get("labs", {})
    weeks = patient_data.get("weeks") or 20  # Default to 20 if None
    age = patient_data.get("age")

    # Previous SGA/FGR (small baby) - THH FGR Guideline
    if "previous sga" in combined or "small baby" in combined or "previous fgr" in combined:
        guidelines.append({
            "name": "Previous SGA/FGR",
            "code": "THH-FGR",
            "summary": "Risk of recurrence. Aspirin 150mg, uterine artery Dopplers, serial growth scans. IOL at 39/40 unless other concerns.",
            "actions": [
                {"text": "Aspirin 150mg from 12 weeks (if <20w)", "ref": "THH-FGR", "default": weeks <= 20},
                {"text": "Assess risk factors for FGR (RCOG stratification)", "ref": "THH-FGR", "default": True}
            ],
            "tests": [{"text": "Uterine artery Doppler", "timing": "20-24 weeks", "ref": "THH-FGR"}],
            "ultrasound": [
                {"text": "Serial growth scans 4-weekly", "timing": "From 28 weeks till birth", "ref": "THH-FGR"}
            ],
            "followup": [
                {"text": "Consultant-led care", "timing": "Ongoing", "ref": "THH-FGR"},
                {"text": "Fetal Medicine referral if EFW <3rd centile", "timing": "If needed", "ref": "THH-FGR"}
            ],
            "clarify": [
                "What was the birthweight and gestation of previous SGA baby?",
                "Was there placental dysfunction (abruption, pre-eclampsia)?",
                "Were uterine artery Dopplers abnormal previously?"
            ],
            "decisions": [
                {"question": "EFW at anomaly scan?", "options": ["≥10th centile → serial scans from 32w", "<10th centile → FGR pathway"]}
            ],
            "plan": [
                (12, "Start Aspirin 150mg if not already"),
                (20, "Uterine artery Dopplers at anomaly scan"),
                (28, "Growth scan"),
                (32, "Growth scan"),
                (36, "Growth scan"),
                (39, "Plan IOL unless other concerns")
            ]
        })

    # Current SGA
    if "current sga" in combined or "small for dates" in combined:
        guidelines.append({
            "name": "Current SGA/FGR",
            "code": "THH-FGR",
            "summary": "EFW/AC <10th centile. Follow FGR pathway with serial monitoring.",
            "tests": [{"text": "Umbilical artery Doppler", "timing": "Serial monitoring", "ref": "THH-FGR"}],
            "ultrasound": [{"text": "Growth + Dopplers", "timing": "2-4 weekly per pathway", "ref": "THH-FGR"}],
            "followup": [{"text": "Fetal medicine referral if <3rd centile", "timing": "Urgent", "ref": "THH-FGR"}],
            "plan": [(weeks, "FGR pathway assessment"), (weeks+2, "Repeat scan + Dopplers"), (39, "Consider IOL")]
        })

    # Anaemia - THH Anaemia and Ferinject guideline
    if "anaemia" in combined or "anemia" in combined:
        guidelines.append({
            "name": "Anaemia in Pregnancy",
            "code": "THH-ANC",
            "summary": "1st trimester <110g/l, 2nd/3rd <105g/l. Oral iron first line, Ferinject if not tolerating.",
            "actions": [
                {"text": "Start oral iron (unless haemoglobinopathy - check ferritin first)", "ref": "THH-ANC", "default": True},
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

    # Pre-eclampsia Risk - THH Antenatal Hypertension guideline
    if "pre-eclampsia" in combined or "preeclampsia" in combined or "previous pet" in combined:
        guidelines.append({
            "name": "Previous Pre-eclampsia",
            "code": "THH-ANC",
            "summary": "Aspirin 150mg from 12w, digital BP monitoring, uterine artery Dopplers, individualised care.",
            "actions": [
                {"text": "Aspirin 150mg from 12 weeks", "ref": "NG133", "default": weeks <= 36},
                {"text": "Digital BP should be used at all times", "ref": "THH-ANC", "default": True}
            ],
            "tests": [
                {"text": "BP and urine each visit (2-4 weekly intervals)", "ref": "THH-ANC"},
                {"text": "Booking bloods incl FBC and U&E – repeat 28 and 34 weeks", "ref": "THH-ANC"}
            ],
            "ultrasound": [
                {"text": "Anomaly + uterine artery Doppler", "timing": "20 weeks", "ref": "THH-ANC"},
                {"text": "Serial growth scans", "timing": "From 28-32w depending on UA Doppler", "ref": "THH-ANC"}
            ],
            "plan": [(20, "Anomaly + UA Doppler"), (28, "Growth scan if abnormal UA"), (32, "Growth scan"), (36, "Growth scan")]
        })

    # Obstetric Cholestasis
    if "cholestasis" in combined:
        guidelines.append({
            "name": "Obstetric Cholestasis",
            "code": "GTG43",
            "summary": "Bile acids monitoring, ursodeoxycholic acid, delivery planning.",
            "actions": [
                {"text": "Start Ursodeoxycholic acid", "ref": "GTG43", "default": True},
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
                {"text": "Folic acid 5mg throughout pregnancy", "ref": "THH-ANC", "default": True},
                {"text": "Consider Vitamin D", "ref": "THH-ANC", "default": True},
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

    # Thrombocytopenia - THH Introduction guidelines
    if "thrombocytopenia" in combined or "low platelets" in combined:
        guidelines.append({
            "name": "Thrombocytopenia",
            "code": "THH-ANC",
            "summary": "ITP: refer to obstetric medicine. Gestational: refer if platelets <80. No scans indicated.",
            "actions": [{"text": "Refer to obstetric medicine at booking (if ITP)", "ref": "THH-ANC", "default": True}],
            "tests": [
                {"text": "FBC, blood film, reticulocyte count", "timing": "Now", "ref": "THH-ANC"},
                {"text": "LFT, TFT, DAT, APS ab, ANA", "timing": "If platelets <80", "ref": "THH-ANC"},
                {"text": "HIV, HepB, HepC, H. pylori", "timing": "If platelets <80", "ref": "THH-ANC"},
                {"text": "FBC every 2 weeks from 34w if <100", "timing": "From 34 weeks", "ref": "THH-ANC"}
            ],
            "followup": [
                {"text": "Obstetric medicine review", "timing": "If platelets <80", "ref": "THH-ANC"}
            ],
            "plan": [(34, "FBC every 2 weeks if platelets <100")]
        })

    # VTE / Previous DVT - THH VTE Prophylaxis flowchart
    if "dvt" in combined or "vte" in combined or "thrombosis" in combined:
        guidelines.append({
            "name": "Previous VTE - HIGH RISK",
            "code": "THH-VTE",
            "summary": "Any previous VTE = HIGH RISK. Requires antenatal LMWH prophylaxis. Refer to thrombosis expert.",
            "actions": [
                {"text": "Start antenatal prophylaxis with LMWH", "ref": "THH-VTE", "default": True},
                {"text": "At least 6 weeks postnatal prophylactic LMWH", "ref": "THH-VTE", "default": True}
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
                {"text": "Folic acid 5mg daily (preconception)", "ref": "THH-Epilepsy", "default": True},
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
                    {"text": "Folic acid 5mg preconception", "ref": "THH-BMI", "default": True},
                    {"text": "VTE and FGR risk assessment at booking", "ref": "THH-BMI", "default": True},
                    {"text": "Vitamin D 25mcg or 1000IU", "ref": "THH-BMI", "default": True},
                    {"text": "Start LMWH (4+ risk factors = from first trimester)", "ref": "THH-VTE", "default": True},
                    {"text": "Assess if equipment can adjust to patient", "ref": "THH-BMI", "default": True}
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
                    {"text": "Folic acid 5mg preconception", "ref": "THH-BMI", "default": True},
                    {"text": "VTE and FGR risk assessment at booking", "ref": "THH-BMI", "default": True},
                    {"text": "Vitamin D 25mcg or 1000IU", "ref": "THH-BMI", "default": True},
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
                {"text": "Joint diabetes clinic referral", "ref": "NG3", "default": True},
                {"text": "Home glucose monitoring", "ref": "NG3", "default": True}
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

    # Previous Caesarean - THH VBAC guideline
    if "caesarean" in combined or "c-section" in combined or "c section" in combined:
        guidelines.append({
            "name": "Previous Caesarean Section",
            "code": "THH-VBAC",
            "summary": "RCOG leaflet for VBAC vs CS. Birth options clinic at 16w. Mode of birth discussion at 36w.",
            "actions": [
                {"text": "Provide RCOG VBAC leaflet at booking/16w", "ref": "THH-VBAC", "default": True}
            ],
            "followup": [
                {"text": "Birth options clinic with Senior MW (if 1 uncomplicated CS)", "timing": "16 weeks", "ref": "THH-VBAC"},
                {"text": "16w ANC with obstetrician (if 2+ uterine surgeries or complex)", "timing": "16 weeks", "ref": "THH-VBAC"},
                {"text": "36w Obstetrician ANC - Mode of Birth", "timing": "36 weeks", "ref": "THH-VBAC"}
            ],
            "plan": [(16, "Birth options clinic / Obs ANC"), (36, "Mode of Birth discussion")]
        })

    # Advanced Maternal Age >40
    if age and age >= 40:
        guidelines.append({
            "name": "Advanced Maternal Age (>40)",
            "code": "THH-ANC",
            "summary": "Aspirin risk assessment at 12w. Obs ANC at 16, 32, 36w. Offer IOL from 39w.",
            "actions": [
                {"text": "Aspirin risk assessment at 12 weeks", "ref": "THH-ANC", "default": True}
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
        # Gestation quick select
        st.markdown("**Gestation**")
        g_cols = st.columns(4)
        selected_weeks = None
        for col, wks in zip(g_cols, [16, 24, 28, 36]):
            if col.button(f"{wks}w", key=f"w{wks}", use_container_width=True):
                selected_weeks = wks

        # Conditions
        st.markdown("**Conditions**")
        conditions = ["Previous SGA", "Anaemia", "Previous Pre-eclampsia", "Twins"]
        selected_conditions = []
        cols = st.columns(2)
        for i, cond in enumerate(conditions):
            if cols[i % 2].checkbox(cond, key=f"cond_{cond}"):
                selected_conditions.append(cond)

        # Text + voice input at bottom
        st.markdown("**Describe scenario**")
        input_cols = st.columns([0.85, 0.15])
        free_text = input_cols[0].text_area(
            "Scenario",
            height=80,
            placeholder="e.g., 32yo G2P1, previous C-section, BMI 35, on aspirin...",
            label_visibility="collapsed"
        )
        with input_cols[1]:
            audio = st.audio_input("🎤", label_visibility="collapsed")

        if audio:
            st.caption("🎤 *Audio captured*")

        # Build custom scenario
        custom_parts = []
        if selected_weeks:
            custom_parts.append(f"{selected_weeks} weeks")
        if selected_conditions:
            custom_parts.append(", ".join(selected_conditions))
        if free_text:
            custom_parts.append(free_text)
        custom_scenario = ", ".join(custom_parts) if custom_parts else ""

        if custom_scenario:
            if st.button("Analyze Custom", type="primary", use_container_width=True):
                st.session_state.scenario_text = custom_scenario
                st.session_state.patient_data = parse_scenario(custom_scenario)
                st.session_state.guidelines = get_applicable_guidelines(
                    st.session_state.patient_data,
                    custom_scenario
                )
                st.session_state.analyzed = True
                st.rerun()

# ================================================================
# MAIN PANEL
# ================================================================
st.title("Clinical Decision Support")

if not st.session_state.analyzed:
    # Welcome message
    st.markdown("## Summary")
    st.info("""
**Welcome to Clinical Decision Support**

This tool provides **explainable, guideline-based recommendations** for antenatal care.

**How to use:**
1. Select gestation and conditions from the left panel
2. Or enter a free-text clinical scenario
3. Click **Analyze** to generate recommendations

**Features:**
- ✅ Evidence-based guidelines (NICE, RCOG)
- ✅ Transparent recommendations with source references
- ✅ Customizable - select/deselect relevant guidelines
- ✅ Tests, ultrasound, and follow-up checklists
- ✅ Patient leaflets for shared decision-making
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
        all_followup.extend(g.get("followup", []))
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

        selected_actions = []
        if guidelines:
            for g in guidelines:
                with st.expander(f"📁 {g['name']}", expanded=False):
                    st.caption(f"*{g['summary']}*")
                    st.divider()
                    for idx, action in enumerate(g.get("actions", [])):
                        key = f"act_{g['code']}_{g['name'][:5]}_{idx}"
                        is_selected = st.checkbox(
                            f"{action['text']} {make_link(action['ref'])}",
                            value=action.get("default", False),
                            key=key
                        )
                        if is_selected:
                            selected_actions.append(action['text'])
        else:
            st.caption("No specific guidelines triggered. Add more details.")

        # 🧪 TESTS (Checkboxes)
        st.markdown("## 🧪 Tests")
        selected_tests = []
        if all_tests:
            for i, t in enumerate(all_tests):
                key = f"test_{t['text'][:20]}_{i}"
                is_selected = st.checkbox(
                    f"**{t['text']}** — *{t['timing']}* {make_link(t['ref'])}",
                    key=key,
                    value=False
                )
                if is_selected:
                    selected_tests.append(t['text'])
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
        if selected_actions or selected_tests:
            st.markdown("## ✅ Selected Actions")
            st.caption("*Items you've selected from guidelines and tests:*")
            if selected_actions:
                for action in selected_actions:
                    st.markdown(f"• {action}")
            if selected_tests:
                for test in selected_tests:
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
            selected_items = selected_actions + [f"TEST: {t}" for t in selected_tests]

            txt = f"""SUMMARY | {datetime.now().strftime('%d/%m/%Y')}
{weeks}w | {patient_data.get('parity', '-')} | Age {patient_data.get('age', '?')}
Risks: {', '.join(unique_risks) or 'None'}
Guidelines: {', '.join([g['name'] for g in guidelines]) or 'None'}

SELECTED ACTIONS: {'; '.join(selected_items) or 'None selected'}
TESTS: {'; '.join([t['text'] for t in all_tests]) or 'Routine'}
ULTRASOUND: {'; '.join([s['text'] for s in all_ultrasound]) or 'Routine'}
FOLLOW UP: {'; '.join(merged_fu_texts) or 'Routine'}
"""
            st.code(txt, language=None)

        st.caption("⚠️ Decision support only. Verify against current guidelines.")

    # ================================================================
    # TAB 2: PATIENT-LED CARE
    # ================================================================
    with tab_patient:
        st.markdown("## 👤 Patient-led Care")
        st.markdown("*Resources and leaflets to share with the patient for informed decision-making.*")

        # Patient-friendly summary
        st.markdown("### 📝 Your Care Summary")
        st.caption("*A simple explanation of your care plan:*")

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

        # Display patient summary
        if patient_summary:
            st.info("\n".join(patient_summary))
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
                    col1.checkbox("", key=f"leaf_nice_{l['title'][:20]}", label_visibility="collapsed")
                    col2.markdown(f"[{l['title']}]({l['url']})")

            if rcog_leaflets:
                st.markdown("#### RCOG Patient Information")
                for l in rcog_leaflets:
                    col1, col2 = st.columns([0.05, 0.95])
                    col1.checkbox("", key=f"leaf_rcog_{l['title'][:20]}", label_visibility="collapsed")
                    col2.markdown(f"[{l['title']}]({l['url']})")

            if hillingdon_leaflets:
                st.markdown("#### Hillingdon Hospital Leaflets")
                for l in hillingdon_leaflets:
                    col1, col2 = st.columns([0.05, 0.95])
                    col1.checkbox("", key=f"leaf_hil_{l['title'][:20]}", label_visibility="collapsed")
                    col2.markdown(f"[{l['title']}]({l['url']})")

            if other_leaflets:
                st.markdown("#### Other Resources")
                for l in other_leaflets:
                    col1, col2 = st.columns([0.05, 0.95])
                    col1.checkbox("", key=f"leaf_other_{l['title'][:20]}", label_visibility="collapsed")
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
