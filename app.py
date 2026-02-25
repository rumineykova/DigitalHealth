"""
Clinical Decision Support System - Compact View
"""

import streamlit as st
import json
import os
from datetime import datetime
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guidelines.antenatal_care import get_appointment_by_week, check_antenatal_red_flags

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
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

# Compact patient database
PATIENTS = {
    "P005": {"name": "Emma Davis", "age": 32, "weeks": 16, "parity": "G2P1",
             "risks": ["Previous pre-eclampsia"], "labs": {"Hb": 108, "BP": "125/80"}},
    "P006": {"name": "Lisa Martinez", "age": 35, "weeks": 12, "parity": "G3P2",
             "risks": ["BMI 38.5", "Previous GDM"], "labs": {"Hb": 125, "BP": "130/85"}},
    "P007": {"name": "Rachel Green", "age": 30, "weeks": 20, "parity": "G1P0",
             "risks": ["DCDA twins", "Rh negative"], "labs": {"Hb": 105, "BP": "115/70"}},
    "P008": {"name": "Priya Patel", "age": 34, "weeks": 30, "parity": "G2P1",
             "risks": ["GDM diagnosed"], "labs": {"Hb": 118, "BP": "122/78"}},
    "P009": {"name": "Amy Wilson", "age": 27, "weeks": 34, "parity": "G1P0",
             "risks": ["Reduced movements"], "labs": {"Hb": 112, "BP": "118/74"}},
    "P010": {"name": "Fatima Ahmed", "age": 29, "weeks": 28, "parity": "G4P3",
             "risks": ["Anaemia Hb 92"], "labs": {"Hb": 92, "BP": "110/65"}},
    "P011": {"name": "Sophie Brown", "age": 31, "weeks": 41, "parity": "G2P1",
             "risks": ["Postdates"], "labs": {"Hb": 120, "BP": "115/72"}},
    "P012": {"name": "Hannah Clarke", "age": 33, "weeks": 36, "parity": "G1P0",
             "risks": ["Breech"], "labs": {"Hb": 116, "BP": "112/68"}},
}

def parse_input(text):
    text_lower = text.lower()
    result = {"weeks": None, "risks": [], "symptoms": []}

    # Extract weeks
    m = re.search(r'(\d+)\s*weeks?', text_lower)
    if m:
        result["weeks"] = int(m.group(1))

    # Extract risks
    risk_map = {
        "pre-eclampsia": "Previous pre-eclampsia", "preeclampsia": "Previous pre-eclampsia",
        "gdm": "GDM risk", "gestational diabetes": "GDM risk", "bmi 3": "High BMI",
        "twins": "Multiple pregnancy", "rh neg": "Rh negative",
        "anaemia": "Anaemia", "anemia": "Anaemia", "hb 9": "Anaemia",
        "reduced movement": "Reduced movements", "breech": "Breech",
        "postdates": "Postdates", "41 week": "Postdates", "42 week": "Postdates"
    }
    for kw, risk in risk_map.items():
        if kw in text_lower and risk not in result["risks"]:
            result["risks"].append(risk)

    # Symptoms
    for s in ["headache", "visual", "bleeding", "pain", "swelling"]:
        if s in text_lower:
            result["symptoms"].append(s)

    return result

def get_recommendations(weeks, risks, symptoms):
    """Generate compact recommendations"""
    recs = {
        "alerts": [],
        "actions": [],
        "tests": [],
        "decisions": [],
        "followup": None,
        "info_needed": []
    }

    # RED FLAGS
    if symptoms:
        if "bleeding" in symptoms:
            recs["alerts"].append(("Vaginal bleeding - urgent assessment", "NG201 1.1"))
        if "headache" in symptoms or "visual" in symptoms:
            recs["alerts"].append(("Possible pre-eclampsia - check BP urgently", "NG133 1.3"))

    # PRE-ECLAMPSIA PATHWAY
    if any("pre-eclampsia" in r.lower() for r in risks):
        recs["actions"].extend([
            ("Start Aspirin 150mg nocte", "From 12w to 36w", "NG133 1.1.2"),
            ("Consultant-led care", "Refer at booking", "NG201 1.2.5"),
        ])
        recs["tests"].extend([
            ("BP monitoring", "2-4 weekly → weekly from 32w", "NG133 1.2"),
            ("Urinalysis", "Each visit", "NG201 1.3"),
            ("Growth scans", "28, 32, 36 weeks", "NG201 1.4"),
        ])
        recs["decisions"].append({
            "q": "Previous pre-eclampsia severity?",
            "opts": [
                ("Early-onset (<34w)", ["Maternal medicine referral", "Uterine artery Doppler 20-24w", "Serial scans from 26w"], "NG133 1.1.3"),
                ("Late-onset (>34w)", ["Shared care acceptable", "Growth scans 28/32/36w", "Extra BP monitoring from 24w"], "NG133 1.1.4"),
                ("HELLP/Eclampsia", ["URGENT maternal medicine", "Consider thromboprophylaxis", "Intensive monitoring"], "NG133 1.1.5"),
            ]
        })
        recs["info_needed"].append("Gestation at previous pre-eclampsia onset?")
        recs["followup"] = ("2-4 weekly → weekly from 32w", "High-risk")

    # GDM / HIGH BMI PATHWAY
    if any("gdm" in r.lower() or "bmi" in r.lower() for r in risks):
        recs["actions"].append(("Dietitian referral", "First trimester", "NG3 1.2"))
        recs["tests"].append(("GTT 75g", "Booking if prev GDM; 24-28w if BMI≥30", "NG3 1.2.4"))
        recs["decisions"].append({
            "q": "GTT result?",
            "opts": [
                ("Normal", ["Routine care", "No repeat GTT needed"], "NG3 1.2"),
                ("GDM diagnosed", ["Joint diabetes clinic", "SMBG 4x daily", "Targets: fasting <5.3, 1hr <7.8"], "NG3 1.4"),
            ]
        })
        if any("bmi" in r.lower() for r in risks):
            recs["actions"].append(("Anaesthetic review", "Third trimester", "NG201 1.5"))
            recs["actions"].append(("VTE risk assessment", "Consider LMWH", "NG201 1.6"))
        recs["followup"] = ("4-weekly; 1-2 weekly if GDM", "Metabolic risk")

    # RH NEGATIVE
    if any("rh neg" in r.lower() for r in risks):
        recs["actions"].append(("Anti-D 1500 IU", "At 28 weeks", "NG201 1.6.1"))
        recs["tests"].append(("Antibody screen", "Booking + 28w", "NG201 1.2.3"))
        recs["decisions"].append({
            "q": "Sensitising event?",
            "opts": [
                ("<20 weeks", ["Anti-D 250 IU within 72hrs", "No Kleihauer"], "NG201 1.6.2"),
                (">20 weeks", ["Anti-D 500 IU within 72hrs", "Kleihauer test", "Extra anti-D if positive"], "NG201 1.6.3"),
            ]
        })

    # TWINS
    if any("twin" in r.lower() or "multiple" in r.lower() for r in risks):
        recs["actions"].append(("Multiple pregnancy team referral", "By 14 weeks", "NG137 1.1"))
        recs["decisions"].append({
            "q": "Chorionicity?",
            "opts": [
                ("DCDA", ["Scans 4-weekly from 24w", "Deliver 37+0-37+6"], "NG137 1.3"),
                ("MCDA", ["Scans 2-weekly from 16w", "TTTS surveillance", "Deliver 36+0-36+6"], "NG137 1.4"),
                ("MCMA", ["Fetal medicine referral", "Consider admission 26-28w", "Deliver 32-34w"], "NG137 1.5"),
            ]
        })
        recs["followup"] = ("Per chorionicity protocol", "Multiple pregnancy")

    # ANAEMIA
    if any("anaemia" in r.lower() or "anemia" in r.lower() for r in risks):
        recs["tests"].append(("FBC + ferritin", "Now + 2-4w post-treatment", "NG201 1.7"))
        recs["decisions"].append({
            "q": "Hb level?",
            "opts": [
                ("100-109 (mild)", ["Oral iron BD", "Dietary advice", "Recheck 2-4w"], "NG201 1.7.1"),
                ("70-99 (moderate)", ["Oral iron BD", "Consider IV iron if no response", "Recheck 2w"], "NG201 1.7.2"),
                ("<70 (severe)", ["Urgent haematology", "IV iron/transfusion", "Daily monitoring"], "NG201 1.7.3"),
            ]
        })

    # REDUCED MOVEMENTS
    if any("movement" in r.lower() for r in risks):
        recs["alerts"].append(("Reduced fetal movements - same day assessment", "RCOG GTG57"))
        recs["actions"].append(("CTG monitoring", "Minimum 20 mins", "GTG57 4"))
        recs["decisions"].append({
            "q": "CTG result?",
            "opts": [
                ("Normal", ["Reassure", "Return if no improvement 24hrs"], "GTG57 5.1"),
                ("Suspicious", ["Senior review", "Ultrasound for liquor/growth"], "GTG57 5.2"),
                ("Pathological", ["IMMEDIATE obstetric review", "Consider delivery"], "GTG57 5.3"),
                ("Recurrent RFM", ["Growth scan <24hrs", "Increased surveillance"], "GTG57 6"),
            ]
        })

    # BREECH
    if any("breech" in r.lower() for r in risks):
        recs["actions"].append(("Confirm with ultrasound", "If not done", "NG201 1.8"))
        recs["decisions"].append({
            "q": "ECV decision?",
            "opts": [
                ("Accepts ECV", ["Book ECV 36-37w", "FBC + G&S", "Anti-D if Rh neg"], "GTG20a 3"),
                ("Declines ECV", ["Discuss vaginal breech vs caesarean", "Consultant review"], "GTG20b 4"),
            ]
        })

    # POSTDATES
    if any("postdates" in r.lower() for r in risks) or (weeks and weeks >= 41):
        recs["actions"].append(("Offer membrane sweep", "40w (nullip) / 41w (all)", "NG207 1.2"))
        recs["decisions"].append({
            "q": "IOL preference?",
            "opts": [
                ("Accepts IOL", ["Book IOL 41+0 to 42+0", "Explain process"], "NG207 1.3"),
                ("Declines IOL", ["Twice-weekly CTG+AFI from 42w", "Daily movement monitoring"], "NG207 1.4"),
            ]
        })

    # Default follow-up
    if not recs["followup"] and weeks:
        if weeks < 28:
            recs["followup"] = ("4 weeks", "Routine")
        elif weeks < 36:
            recs["followup"] = ("2-3 weeks", "Routine")
        else:
            recs["followup"] = ("Weekly", "Late pregnancy")

    return recs

def format_summary(recs, patient="", weeks=None):
    """Compact copy-paste summary"""
    lines = [f"SUMMARY | {datetime.now().strftime('%d/%m/%Y %H:%M')}"]
    if patient:
        lines.append(f"Patient: {patient}" + (f" | {weeks}w" if weeks else ""))

    if recs["alerts"]:
        lines.append("\n⚠️ ALERTS: " + "; ".join([a[0] for a in recs["alerts"]]))

    if recs["actions"]:
        lines.append("\n✅ ACTIONS:")
        for a in recs["actions"]:
            lines.append(f"  □ {a[0]} ({a[1]}) [{a[2]}]")

    if recs["tests"]:
        lines.append("\n🧪 TESTS:")
        for t in recs["tests"]:
            lines.append(f"  □ {t[0]} - {t[1]} [{t[2]}]")

    if recs["followup"]:
        lines.append(f"\n📅 FOLLOW-UP: {recs['followup'][0]} ({recs['followup'][1]})")

    if recs["info_needed"]:
        lines.append("\n❓ CLARIFY: " + "; ".join(recs["info_needed"]))

    return "\n".join(lines)

# === UI ===

st.title("Clinical Decision Support")

# Sidebar - compact
with st.sidebar:
    st.subheader("Patient")
    opts = ["None"] + [f"{k}: {v['name']} ({v['weeks']}w)" for k, v in PATIENTS.items()]
    sel = st.selectbox("Select", opts, label_visibility="collapsed")

    if sel != "None":
        pid = sel.split(":")[0]
        st.session_state.current_patient = pid
        p = PATIENTS[pid]
        st.caption(f"**{p['name']}** | {p['age']}y | {p['parity']} | {p['weeks']}w")
        if p["risks"]:
            st.warning(" | ".join(p["risks"]))
        st.caption(f"Labs: Hb {p['labs']['Hb']}, BP {p['labs']['BP']}")
    else:
        st.session_state.current_patient = None

# Quick buttons - single row
cols = st.columns(6)
scenarios = [
    ("Pre-eclampsia", "16 weeks with previous pre-eclampsia"),
    ("GDM Risk", "28 weeks, BMI 35, need GTT?"),
    ("RFM", "34 weeks reduced movements"),
    ("Rh Neg", "Rh negative 28 weeks"),
    ("Twins", "DCDA twins 20 weeks"),
    ("Anaemia", "28 weeks Hb 92"),
]
for i, (label, query) in enumerate(scenarios):
    if cols[i].button(label, use_container_width=True):
        st.session_state.quick = query

# Input
default = st.session_state.pop("quick", "")
query = st.text_input("Enter clinical query:", value=default,
                       placeholder="e.g., 16 weeks with previous pre-eclampsia, what monitoring?")

if st.button("Analyze", type="primary") and query:
    parsed = parse_input(query)

    # Merge patient data
    patient_name = ""
    if st.session_state.current_patient:
        p = PATIENTS[st.session_state.current_patient]
        patient_name = p["name"]
        if not parsed["weeks"]:
            parsed["weeks"] = p["weeks"]
        parsed["risks"].extend([r for r in p["risks"] if r not in parsed["risks"]])

    recs = get_recommendations(parsed["weeks"], parsed["risks"], parsed["symptoms"])

    # Save history
    st.session_state.history.append({"ts": datetime.now().isoformat(), "q": query, "risks": parsed["risks"]})
    save_json(HISTORY_FILE, st.session_state.history[-50:])

    st.divider()

    # === COMPACT OUTPUT ===

    # Alerts - always visible
    if recs["alerts"]:
        for alert, ref in recs["alerts"]:
            st.error(f"⚠️ **{alert}** `{ref}`")

    # Actions - compact list with expand
    if recs["actions"]:
        st.markdown("### ✅ Actions")
        for action, timing, ref in recs["actions"]:
            st.markdown(f"• **{action}** — _{timing}_ `{ref}`")

    # Tests - compact
    if recs["tests"]:
        st.markdown("### 🧪 Tests")
        for test, freq, ref in recs["tests"]:
            st.markdown(f"• **{test}** — _{freq}_ `{ref}`")

    # Follow-up - one line
    if recs["followup"]:
        st.info(f"📅 **Follow-up:** {recs['followup'][0]} ({recs['followup'][1]})")

    # Info needed - compact
    if recs["info_needed"]:
        st.warning("❓ **Clarify:** " + " • ".join(recs["info_needed"]))

    # Decision trees - collapsed by default
    if recs["decisions"]:
        with st.expander("🔀 Decision Points (click to expand)"):
            for dec in recs["decisions"]:
                st.markdown(f"**{dec['q']}**")
                for cond, actions, ref in dec["opts"]:
                    st.markdown(f"  **IF** {cond} **→** {', '.join(actions)} `{ref}`")
                st.markdown("---")

    # Copy summary - collapsed
    with st.expander("📋 Copy Summary"):
        st.code(format_summary(recs, patient_name, parsed["weeks"]), language=None)

    st.caption(f"Source: NICE Guidelines | [NG201](https://www.nice.org.uk/guidance/ng201)")

# History - collapsed
with st.expander("📜 History"):
    for h in reversed(st.session_state.history[-5:]):
        ts = h.get('ts', h.get('timestamp', ''))[:16] if h else ''
        q = h.get('q', h.get('query', ''))[:60] if h else ''
        if ts and q:
            st.caption(f"{ts}: {q}...")
    if st.button("Clear"):
        st.session_state.history = []
        save_json(HISTORY_FILE, [])
        st.rerun()

st.caption("⚠️ Decision support only. Verify against current guidelines.")
