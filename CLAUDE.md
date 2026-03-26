# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Clinical Decision Support System (CDSS)** for antenatal care. The application is a Streamlit-based web interface that provides evidence-based, guideline-driven recommendations for managing high-risk pregnancies.

The system parses free-text patient scenarios (e.g., "24yo with epilepsy, 16 weeks pregnant, on lamotrigine") and generates actionable clinical recommendations including:
- Applicable clinical guidelines (NICE, RCOG Green-top, local Hillingdon/THH protocols)
- Required tests and investigations
- Ultrasound scan schedules
- Follow-up referrals and specialist care
- Patient information leaflets
- Timeline-based care planning

## Running the Application

**Start the app:**
```bash
streamlit run app.py
```

**Dependencies:**
- Install requirements: `pip install -r requirements_pip.txt`
- Python 3.14+ (tested with venv at `./venv`)
- Only dependency: `streamlit>=1.28.0`

**Data persistence:**
- Conversation history and patient states are saved to JSON files in `data/`
- This folder is gitignored but created automatically on first run

## Architecture

### Single-File Design
The entire application is in `app.py` (~1150 lines). This is intentional for a prototype/demo system. All logic—UI, parsing, guideline matching, formatting—lives in one file.

### Key Data Structures

**1. Guideline URLs (`GUIDELINE_URLS` dict, lines 112-149)**
- Maps guideline codes (e.g., "NG201", "GTG68", "THH-Epilepsy") to URLs
- National guidelines: NICE (NG*) and RCOG Green-top (GTG*)
- Local guidelines: Hillingdon Hospital (THH-*) stored on SharePoint
- Used by `make_link()` to generate markdown hyperlinks in the UI

**2. Patient Leaflets Database (`PATIENT_LEAFLETS` dict, lines 51-105)**
- Organized by condition tags (e.g., "epilepsy", "vte", "pre-eclampsia")
- Each entry contains title, source (NICE/RCOG/Hillingdon), and URL
- Displayed in the "Patient-led Care" tab for shared decision-making

**3. Demo Use Cases (`DEMO_USE_CASES` dict, lines 42-48)**
- Predefined clinical scenarios for quick testing
- Auto-selected on app load for ease of demonstration

**4. Guideline Structure (returned by `get_applicable_guidelines()`, lines 213-627)**
Each guideline is a dictionary with:
- `name`: Display name
- `code`: Guideline reference code
- `summary`: One-line clinical summary
- `actions`: List of actionable items (with `default` checkbox state)
- `tests`: Required investigations with timing
- `ultrasound`: Scan schedule
- `followup`: Referrals and specialist appointments
- `clarify`: Questions to ask the patient for individualization
- `decisions`: Clinical decision trees (if/then logic)
- `plan`: Timeline of actions by gestational week

### Core Functions

**`parse_scenario(text)` (lines 158-211)**
- Regex-based parser for free-text input
- Extracts: age, gestational weeks, BMI, parity, medical conditions
- Returns structured `patient_data` dict with `risks[]` and `leaflet_tags[]`
- Pattern matching is intentionally simple (not NLP) for transparency

**`get_applicable_guidelines(patient_data, risks_text)` (lines 213-627)**
- **This is the clinical decision engine**
- Takes parsed patient data and returns applicable guidelines
- Each condition (e.g., "Previous SGA", "Epilepsy", "BMI ≥40") has its own guideline block
- Guidelines are aligned with the Hillingdon "Antenatal Care Schedule" PDF
- Key conditions handled:
  - Previous SGA/FGR (lines 222-255)
  - Anaemia (lines 270-286)
  - Pre-eclampsia risk (lines 289-307)
  - Obstetric cholestasis (lines 310-325)
  - Multiple pregnancy (lines 328-352)
  - Thrombocytopenia (lines 355-371)
  - VTE/DVT (lines 374-403)
  - Epilepsy (lines 405-443)
  - High BMI (lines 446-528, with 3 tiers: ≥40, 35-39.9, 30-34.9)
  - GDM (lines 531-550)
  - Previous Caesarean (lines 553-567)
  - Advanced maternal age >40 (lines 570-586)
  - Previous preterm labour (lines 589-625)

**`get_leaflets_for_patient(leaflet_tags)` (lines 629-644)**
- Maps condition tags to patient information leaflets
- Deduplicates and returns unique leaflets
- Always includes "general" antenatal leaflets

**`make_link(ref)` (lines 151-156)**
- Converts guideline reference codes into clickable markdown links
- Matches codes against `GUIDELINE_URLS` dictionary

### UI Structure

**Streamlit session state (lines 26-39):**
- `history`: List of previous queries (persisted to `data/conversation_history.json`)
- `analyzed`: Boolean flag for whether analysis has run
- `scenario_text`: Current scenario text
- `patient_data`: Parsed patient data dict
- `guidelines`: List of applicable guidelines
- `selected_actions`, `selected_tests`: User selections (checkboxes)

**Sidebar (lines 649-741):**
- Demo use case selector (dropdown)
- "Analyze" button triggers parsing and guideline matching
- Custom scenario builder (collapsed by default):
  - Quick gestation buttons (16w, 24w, 28w, 36w)
  - Condition checkboxes
  - Free text area + voice input (audio widget)

**Main panel with 2 tabs (lines 833-1150):**

1. **📋 Clinical Care tab (lines 838-998)**
   - Summary box: patient demographics, risks, applicable guidelines
   - Guidelines: Expandable sections with checkboxes for actions
   - Tests: Checkboxes for investigations (default unchecked)
   - Ultrasound: Scan schedule (read-only)
   - Follow Up: Referrals and specialist care
   - Clarify: Questions to individualize care (collapsible)
   - Decision Points: If/then clinical logic (collapsible)
   - Plan & Management: Timeline view by gestational week (collapsible)
   - Selected Actions: Dynamic summary of checked items
   - Copy Summary: Plain text export for medical records

2. **👤 Patient-led Care tab (lines 1004-1150)**
   - Patient-friendly summary in lay language
   - Patient information leaflets grouped by source (NICE/RCOG/Hillingdon)
   - Checkboxes to select leaflets to share
   - Email/Print buttons (UI only, not functional)
   - Discussion points: Key topics to cover with patient

## Important Context

### Clinical Guidelines
The system is based on:
- **NICE guidelines** (NG201 Antenatal care, NG133 Hypertension, NG3 Diabetes, etc.)
- **RCOG Green-top guidelines** (GTG68 Epilepsy, GTG37a/b VTE, GTG72 Obesity, etc.)
- **Local Hillingdon Hospital protocols** (stored on SharePoint, linked in code)

The "Antenatal Care Schedule" PDF in the repo root is the master reference document for local pathways.

### Guideline Alignment
When modifying guidelines:
- Check the `GUIDELINE_URLS` dict to ensure correct references
- Follow the pattern in existing guideline blocks (name, code, summary, actions, tests, ultrasound, followup, plan)
- Include `clarify` questions and `decisions` arrays for complex conditions
- Set `default: True/False` on actions to guide checkbox pre-selection
- Use gestational weeks in `plan` tuples: `(week, "action description")`

### Adding New Conditions
To add a new condition:
1. Add pattern matching in `parse_scenario()` (lines 190-209)
2. Add a new block in `get_applicable_guidelines()` following existing structure
3. Add patient leaflets to `PATIENT_LEAFLETS` if needed
4. Add guideline URL to `GUIDELINE_URLS` with appropriate code

### Patient Parsing
The `parse_scenario()` function uses simple regex matching. This is deliberate for:
- Transparency (no black-box NLP)
- Predictability for clinical users
- Easy debugging and modification

When extending, maintain this pattern-based approach rather than introducing ML/NLP dependencies.

### Data Files
- `data/conversation_history.json`: Recent queries (last 50), saved on each analysis
- `data/patient_states.json`: Placeholder for future patient state persistence (currently unused)
- Both files are gitignored and auto-created

### File Organization
- `app.py`: Main application (this is the only active Python file)
- `app2.py`: Empty placeholder
- `requirements_pip.txt`: Python dependencies
- `requirements.md`: Original user requirements (not technical dependencies)
- `guidelines/`: Folder for guideline documents (if any)
- `Maternity clinical guidelines/`: Local Hillingdon clinical guideline PDFs
- `ANTENATAL CARE SCHEDULE.pdf`: Master reference for local care pathways

## Development Notes

### Streamlit-Specific Patterns
- Use `st.session_state` for all persistent state across reruns
- Checkbox keys must be unique: use format `f"{category}_{identifier}_{index}"`
- `st.rerun()` triggers full page refresh to reflect state changes
- Collapsible sections use `st.expander()` or `with st.expander():`
- Tabs use `st.tabs()` returning tab objects for context managers

### Adding New Guidelines
When adding a new guideline block, ensure:
- The condition trigger is added to `parse_scenario()` or checked in `get_applicable_guidelines()`
- All timing references use gestational weeks (not dates)
- `ref` fields in actions/tests/followup match keys in `GUIDELINE_URLS`
- Patient-friendly explanations are added to the Patient-led Care tab (lines 1024-1042)

### Link Generation
`make_link(ref)` expects refs in format: "CODE text" where CODE matches a key in `GUIDELINE_URLS`. For example:
- `"NG201"` → generates link to NICE NG201
- `"GTG68 Epilepsy"` → generates link to RCOG Green-top 68
- `"THH-FGR"` → generates link to local Hillingdon FGR guideline

### UI Conventions
- Use "**bold**" for emphasis in markdown
- Use "*italics*" for timing/context
- Use "• " (bullet) for lists
- Use `st.caption()` for helper text
- Use `st.info()` for informational blocks
- Use `st.divider()` to separate major sections

## Testing

**Manual testing workflow:**
1. Run `streamlit run app.py`
2. Select a demo use case from sidebar dropdown
3. Click "Analyze"
4. Check that correct guidelines appear
5. Expand guideline sections and verify actions/tests/scans
6. Switch to "Patient-led Care" tab and verify leaflets
7. Test custom scenario builder with different conditions

**Key test cases:**
- Use Case 1: Epilepsy + Lamotrigine (tests drug monitoring, ECHO, growth scans)
- Use Case 2: High BMI + Previous SGA (tests BMI stratification, FGR pathway, VTE risk)
- Use Case 3: Previous Preterm (tests cervical length surveillance, progesterone)
- Use Case 4: High BMI + DVT (tests VTE prophylaxis, LMWH, anaesthetic review)

No automated test suite exists. All testing is manual via the Streamlit UI.
