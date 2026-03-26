<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pregnancy Clinical Decision Support System - Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f8f9fa;
            color: #2c3e50;
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2rem;
            margin-bottom: 10px;
        }

        header p {
            opacity: 0.95;
            font-size: 1.1rem;
        }

        .layout {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 20px;
        }

        .sidebar {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            height: fit-content;
            position: sticky;
            top: 20px;
        }

        .sidebar h2 {
            color: #0066cc;
            font-size: 1.3rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #2c3e50;
        }

        .form-group input[type="text"],
        .form-group input[type="number"],
        .form-group input[type="date"],
        .form-group textarea {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            font-size: 0.95rem;
            transition: border-color 0.2s;
        }

        .form-group input:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #0066cc;
            box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
        }

        .form-group textarea {
            resize: vertical;
            min-height: 80px;
        }

        .checkbox-group {
            margin-bottom: 8px;
        }

        .checkbox-group input[type="checkbox"] {
            margin-right: 8px;
        }

        .checkbox-group label {
            font-weight: 400;
            margin-bottom: 0;
        }

        .btn-primary {
            width: 100%;
            background: #0066cc;
            color: white;
            padding: 14px 20px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 10px;
        }

        .btn-primary:hover {
            background: #0052a3;
        }

        .main-content {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .patient-card {
            background: linear-gradient(to right, #e7f3ff 0%, #f0f7ff 100%);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #0066cc;
            margin-bottom: 25px;
        }

        .patient-card h3 {
            color: #0066cc;
            margin-bottom: 10px;
        }

        .patient-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }

        .patient-info-item {
            display: flex;
            align-items: center;
        }

        .patient-info-item strong {
            margin-right: 6px;
        }

        .alert {
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid;
        }

        .alert-warning {
            background-color: #fff3cd;
            border-color: #ff9800;
            color: #856404;
        }

        .alert-success {
            background-color: #d4edda;
            border-color: #28a745;
            color: #155724;
        }

        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }

        .tab {
            padding: 12px 24px;
            background: transparent;
            border: none;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 600;
            color: #6c757d;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
        }

        .tab:hover {
            color: #0066cc;
            background: #f8f9fa;
        }

        .tab.active {
            color: #0066cc;
            border-bottom-color: #0066cc;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .recommendation-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #cbd5e0;
        }

        .recommendation-item.urgent {
            border-left-color: #ff9800;
            background: #fff8f0;
        }

        .recommendation-item.routine {
            border-left-color: #28a745;
        }

        .recommendation-item h4 {
            color: #2c3e50;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .badge-urgent {
            background: #ff9800;
            color: white;
        }

        .badge-routine {
            background: #28a745;
            color: white;
        }

        .badge-time-sensitive {
            background: #ffc107;
            color: #000;
        }

        .guideline-cite {
            background: #e7f3ff;
            padding: 12px;
            border-radius: 6px;
            margin-top: 10px;
            border-left: 3px solid #0066cc;
            font-size: 0.9rem;
        }

        .guideline-cite strong {
            color: #0066cc;
        }

        .summary-box {
            background: #f0f7ff;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #b3d9ff;
        }

        .summary-box textarea {
            width: 100%;
            min-height: 400px;
            padding: 15px;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            margin-top: 15px;
        }

        .btn-copy {
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 10px;
        }

        .btn-copy:hover {
            background: #218838;
        }

        .welcome-screen {
            text-align: center;
            padding: 60px 20px;
        }

        .welcome-screen h2 {
            color: #0066cc;
            margin-bottom: 20px;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }

        .feature-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: left;
        }

        .feature-card h3 {
            color: #0066cc;
            margin-bottom: 10px;
        }

        .help-text {
            font-size: 0.85rem;
            color: #6c757d;
            margin-top: 4px;
        }

        .section-header {
            color: #2c3e50;
            font-size: 1.3rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }

        footer {
            margin-top: 40px;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9rem;
            border-top: 1px solid #e0e0e0;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏥 Pregnancy Clinical Decision Support System</h1>
            <p>Evidence-based recommendations with explainable AI</p>
        </header>

        <div class="layout">
            <!-- Sidebar -->
            <div class="sidebar">
                <h2>📋 Patient Information</h2>
                <form id="patientForm">
                    <div class="form-group">
                        <label for="patientId">Patient ID</label>
                        <input type="text" id="patientId" placeholder="e.g., MRN-12345">
                    </div>

                    <div class="form-group">
                        <label for="age">Age</label>
                        <input type="number" id="age" min="13" max="60" value="30">
                    </div>

                    <h3 style="margin-top: 25px; margin-bottom: 15px; color: #2c3e50; font-size: 1.1rem;">Obstetric History</h3>

                    <div class="form-group">
                        <label for="lmp">Last Menstrual Period (LMP)</label>
                        <input type="date" id="lmp" required>
                        <span class="help-text">First day of last menstrual period</span>
                    </div>

                    <div class="form-group">
                        <label for="gravida">Gravida</label>
                        <input type="number" id="gravida" min="1" max="20" value="1">
                        <span class="help-text">Number of pregnancies including current</span>
                    </div>

                    <div class="form-group">
                        <label for="para">Para</label>
                        <input type="number" id="para" min="0" max="20" value="0">
                        <span class="help-text">Number of deliveries ≥20 weeks</span>
                    </div>

                    <h3 style="margin-top: 25px; margin-bottom: 15px; color: #2c3e50; font-size: 1.1rem;">Current Symptoms</h3>

                    <div class="checkbox-group">
                        <input type="checkbox" id="bleeding" name="symptoms">
                        <label for="bleeding">Vaginal bleeding</label>
                    </div>

                    <div class="checkbox-group">
                        <input type="checkbox" id="headache" name="symptoms">
                        <label for="headache">Headache</label>
                    </div>

                    <div class="checkbox-group">
                        <input type="checkbox" id="hypertension" name="symptoms">
                        <label for="hypertension">Known hypertension or elevated BP</label>
                    </div>

                    <div class="checkbox-group">
                        <input type="checkbox" id="decreasedMovement" name="symptoms">
                        <label for="decreasedMovement">Decreased fetal movement (if ≥28 weeks)</label>
                    </div>

                    <div class="form-group" style="margin-top: 15px;">
                        <label for="otherSymptoms">Other symptoms/concerns</label>
                        <textarea id="otherSymptoms" placeholder="e.g., cramping, discharge, contractions..."></textarea>
                    </div>

                    <button type="submit" class="btn-primary">Generate Recommendations</button>
                </form>
            </div>

            <!-- Main Content -->
            <div class="main-content">
                <div id="welcomeScreen" class="welcome-screen">
                    <h2>Welcome to the Clinical Decision Support System</h2>
                    <p style="max-width: 700px; margin: 0 auto; font-size: 1.1rem; line-height: 1.8;">
                        This tool provides evidence-based recommendations for pregnancy care based on ACOG guidelines, 
                        current gestational age, patient symptoms, and standard prenatal care protocols.
                    </p>

                    <div class="feature-grid">
                        <div class="feature-card">
                            <h3>🔬 Laboratory Tests</h3>
                            <p>Gestational age-appropriate screening and diagnostic tests</p>
                        </div>
                        <div class="feature-card">
                            <h3>📊 Imaging Studies</h3>
                            <p>Ultrasound and other imaging recommendations with timing</p>
                        </div>
                        <div class="feature-card">
                            <h3>📅 Follow-up Planning</h3>
                            <p>Next visit scheduling and patient education</p>
                        </div>
                    </div>

                    <div style="margin-top: 40px; padding: 20px; background: #e7f3ff; border-radius: 8px;">
                        <strong>To begin:</strong> Enter patient information in the sidebar and click "Generate Recommendations"
                    </div>
                </div>

                <div id="resultsScreen" class="hidden">
                    <!-- Patient Card -->
                    <div class="patient-card" id="patientCard"></div>

                    <!-- Alerts -->
                    <div id="alertsContainer"></div>

                    <!-- Tabs -->
                    <div class="tabs">
                        <button class="tab active" onclick="switchTab('labs')">🔬 Laboratory Tests</button>
                        <button class="tab" onclick="switchTab('imaging')">📊 Imaging Studies</button>
                        <button class="tab" onclick="switchTab('clarification')">❓ Clarification Needed</button>
                        <button class="tab" onclick="switchTab('followup')">📅 Follow-up Plan</button>
                        <button class="tab" onclick="switchTab('summary')">📄 Clinical Summary</button>
                    </div>

                    <!-- Tab Contents -->
                    <div id="labs" class="tab-content active">
                        <h3 class="section-header">Recommended Laboratory Tests</h3>
                        <div id="labsContent"></div>
                    </div>

                    <div id="imaging" class="tab-content">
                        <h3 class="section-header">Recommended Imaging Studies</h3>
                        <div id="imagingContent"></div>
                    </div>

                    <div id="clarification" class="tab-content">
                        <h3 class="section-header">Information Needed from Patient</h3>
                        <div id="clarificationContent"></div>
                    </div>

                    <div id="followup" class="tab-content">
                        <h3 class="section-header">Follow-up Care Plan</h3>
                        <div id="followupContent"></div>
                    </div>

                    <div id="summary" class="tab-content">
                        <h3 class="section-header">Clinical Summary for Documentation</h3>
                        <div class="summary-box">
                            <p><strong>📋 Copy this summary to your EHR system:</strong></p>
                            <textarea id="summaryText" readonly></textarea>
                            <button class="btn-copy" onclick="copySummary()">📋 Copy to Clipboard</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <strong>Clinical Decision Support Tool Disclaimer:</strong> This system provides clinical decision support based on current evidence-based guidelines. 
            All recommendations should be reviewed by the treating physician in the context of the complete clinical picture. 
            This tool does not replace clinical judgment and is not a substitute for professional medical advice.
        </footer>
    </div>

    <script>
        // Set default LMP to 12 weeks ago
        const today = new Date();
        const twelveWeeksAgo = new Date(today.getTime() - (12 * 7 * 24 * 60 * 60 * 1000));
        document.getElementById('lmp').value = twelveWeeksAgo.toISOString().split('T')[0];

        function calculateGestationalAge(lmpDate) {
            const lmp = new Date(lmpDate);
            const today = new Date();
            const daysPregnant = Math.floor((today - lmp) / (1000 * 60 * 60 * 24));
            const weeks = Math.floor(daysPregnant / 7);
            const days = daysPregnant % 7;
            return { weeks, days };
        }

        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function copySummary() {
            const summaryText = document.getElementById('summaryText');
            summaryText.select();
            document.execCommand('copy');
            alert('Clinical summary copied to clipboard!');
        }

        function generateRecommendations(patientData) {
            const { weeks, days } = patientData.gestationalAge;
            const recommendations = {
                tests: [],
                imaging: [],
                clarification: [],
                followup: [],
                alerts: []
            };

            // First Trimester
            if (weeks <= 13) {
                if (weeks <= 10) {
                    recommendations.tests.push({
                        name: 'Complete Blood Count (CBC)',
                        reason: 'Screen for anemia - standard first trimester workup',
                        guideline: 'ACOG Guidelines for Perinatal Care, 8th Edition',
                        urgency: 'routine'
                    });
                    recommendations.tests.push({
                        name: 'Blood type and Rh status',
                        reason: 'Identify Rh incompatibility risk',
                        guideline: 'ACOG Practice Bulletin No. 181',
                        urgency: 'routine'
                    });
                    recommendations.tests.push({
                        name: 'HIV, Hepatitis B, Syphilis screening',
                        reason: 'Required prenatal infectious disease screening',
                        guideline: 'ACOG/CDC STI screening guidelines',
                        urgency: 'routine'
                    });
                }

                if (weeks >= 7 && weeks <= 13) {
                    recommendations.imaging.push({
                        name: 'Dating ultrasound (transvaginal or transabdominal)',
                        reason: 'Confirm gestational age, assess viability, identify multiple gestation',
                        guideline: 'ACOG Practice Bulletin No. 175: Ultrasound in Pregnancy',
                        timing: `Optimal timing: ${weeks} weeks (current)`,
                        urgency: 'routine'
                    });
                }

                if (weeks >= 11 && weeks <= 13) {
                    recommendations.tests.push({
                        name: 'First trimester combined screening (NT + serum markers)',
                        reason: 'Screen for chromosomal abnormalities (Down syndrome, Trisomy 18)',
                        guideline: 'ACOG Practice Bulletin No. 226',
                        timing: `Window: 11-13+6 weeks (current: ${weeks}+${days})`,
                        urgency: 'time-sensitive'
                    });
                    recommendations.clarification.push({
                        question: 'Has patient expressed preference for prenatal genetic screening?',
                        reason: 'Informed consent needed for first trimester screening or cell-free DNA',
                        action: 'Provide counseling on screening options, benefits, and limitations'
                    });
                }
            }
            // Second Trimester
            else if (weeks >= 14 && weeks <= 27) {
                if (weeks >= 18 && weeks <= 22) {
                    recommendations.imaging.push({
                        name: 'Comprehensive fetal anatomy ultrasound (Level II)',
                        reason: 'Detailed assessment of fetal anatomy, placental location, amniotic fluid',
                        guideline: 'ACOG Practice Bulletin No. 175',
                        timing: `Optimal window: 18-22 weeks (current: ${weeks}+${days})`,
                        urgency: 'routine'
                    });
                }

                if (weeks >= 24 && weeks <= 28) {
                    recommendations.tests.push({
                        name: '1-hour glucose challenge test (50g)',
                        reason: 'Screen for gestational diabetes mellitus',
                        guideline: 'ACOG Practice Bulletin No. 190: Gestational Diabetes',
                        timing: 'Between 24-28 weeks (can be done at current visit)',
                        urgency: 'routine'
                    });
                }
            }
            // Third Trimester
            else {
                if (weeks >= 35 && weeks <= 37) {
                    recommendations.tests.push({
                        name: 'Group B Streptococcus (GBS) vaginal-rectal culture',
                        reason: 'Identify need for intrapartum antibiotic prophylaxis',
                        guideline: 'ACOG Committee Opinion No. 782',
                        timing: 'Between 35-37 weeks',
                        urgency: 'routine'
                    });
                }

                if (weeks >= 28 && weeks <= 32) {
                    recommendations.tests.push({
                        name: 'Complete Blood Count (CBC)',
                        reason: 'Reassess for anemia in third trimester',
                        guideline: 'ACOG Guidelines for Perinatal Care',
                        urgency: 'routine'
                    });
                }
            }

            // Symptom-based
            if (patientData.vaginalBleeding) {
                recommendations.alerts.push({
                    message: '⚠️ VAGINAL BLEEDING REPORTED',
                    action: 'Requires immediate clinical evaluation'
                });

                if (weeks < 20) {
                    recommendations.imaging.push({
                        name: 'Transvaginal ultrasound',
                        reason: 'Assess for viability, rule out ectopic pregnancy, evaluate for subchorionic hemorrhage',
                        guideline: 'ACOG Practice Bulletin No. 200: Early Pregnancy Loss',
                        urgency: 'urgent'
                    });
                }
            }

            if ((patientData.headache || patientData.hypertension) && weeks >= 20) {
                recommendations.alerts.push({
                    message: '⚠️ PREECLAMPSIA RISK - Headache/hypertension after 20 weeks',
                    action: 'Rule out preeclampsia'
                });

                recommendations.tests.push({
                    name: 'Blood pressure measurement',
                    reason: 'Assess for hypertensive disorder of pregnancy',
                    guideline: 'ACOG Practice Bulletin No. 222: Gestational Hypertension and Preeclampsia',
                    urgency: 'urgent'
                });
                recommendations.tests.push({
                    name: 'Urine protein (protein/creatinine ratio or 24-hour collection)',
                    reason: 'Screen for proteinuria (preeclampsia criterion)',
                    guideline: 'ACOG Practice Bulletin No. 222',
                    urgency: 'urgent'
                });
            }

            if (patientData.decreasedMovement && weeks >= 28) {
                recommendations.alerts.push({
                    message: '⚠️ DECREASED FETAL MOVEMENT REPORTED',
                    action: 'Requires same-day evaluation'
                });

                recommendations.imaging.push({
                    name: 'Non-stress test (NST) and ultrasound for AFI/BPP',
                    reason: 'Assess fetal well-being in setting of decreased movement',
                    guideline: 'ACOG Practice Bulletin No. 145: Antepartum Fetal Surveillance',
                    urgency: 'urgent'
                });
            }

            // Follow-up planning
            if (weeks < 28) {
                recommendations.followup.push({
                    action: 'Schedule next prenatal visit',
                    timing: '4 weeks',
                    reason: 'Standard first/second trimester visit interval'
                });
            } else if (weeks < 36) {
                recommendations.followup.push({
                    action: 'Schedule next prenatal visit',
                    timing: '2 weeks',
                    reason: 'Standard third trimester visit interval (28-36 weeks)'
                });
            } else {
                recommendations.followup.push({
                    action: 'Schedule next prenatal visit',
                    timing: '1 week',
                    reason: 'Weekly visits after 36 weeks until delivery'
                });
            }

            return recommendations;
        }

        function renderRecommendations(patientData, recommendations) {
            // Patient Card
            const patientCard = document.getElementById('patientCard');
            patientCard.innerHTML = `
                <h3>👤 Patient Summary</h3>
                <div class="patient-info">
                    <div class="patient-info-item"><strong>ID:</strong> ${patientData.patientId || 'N/A'}</div>
                    <div class="patient-info-item"><strong>Age:</strong> ${patientData.age} years</div>
                    <div class="patient-info-item"><strong>G${patientData.gravida}P${patientData.para}</strong></div>
                    <div class="patient-info-item"><strong>Gestational Age:</strong> ${patientData.gestationalAge.weeks} weeks ${patientData.gestationalAge.days} days</div>
                    <div class="patient-info-item"><strong>LMP:</strong> ${patientData.lmp}</div>
                </div>
            `;

            // Alerts
            const alertsContainer = document.getElementById('alertsContainer');
            alertsContainer.innerHTML = '';
            recommendations.alerts.forEach(alert => {
                alertsContainer.innerHTML += `
                    <div class="alert alert-warning">
                        <strong>${alert.message}</strong><br>
                        Action required: ${alert.action}
                    </div>
                `;
            });

            // Laboratory Tests
            const labsContent = document.getElementById('labsContent');
            if (recommendations.tests.length === 0) {
                labsContent.innerHTML = '<div class="alert alert-success">No laboratory tests recommended at this time based on current gestational age and symptoms.</div>';
            } else {
                labsContent.innerHTML = recommendations.tests.map(test => `
                    <div class="recommendation-item ${test.urgency}">
                        <h4>
                            ${test.name}
                            <span class="badge badge-${test.urgency}">${test.urgency.toUpperCase()}</span>
                        </h4>
                        <p><strong>Indication:</strong> ${test.reason}</p>
                        ${test.timing ? `<p style="color: #0066cc;">⏰ ${test.timing}</p>` : ''}
                        <div class="guideline-cite">
                            <strong>📚 Clinical Guideline:</strong> ${test.guideline}
                        </div>
                    </div>
                `).join('');
            }

            // Imaging Studies
            const imagingContent = document.getElementById('imagingContent');
            if (recommendations.imaging.length === 0) {
                imagingContent.innerHTML = '<div class="alert alert-success">No imaging studies recommended at this time based on current gestational age and symptoms.</div>';
            } else {
                imagingContent.innerHTML = recommendations.imaging.map(study => `
                    <div class="recommendation-item ${study.urgency}">
                        <h4>
                            ${study.name}
                            <span class="badge badge-${study.urgency}">${study.urgency.toUpperCase()}</span>
                        </h4>
                        <p><strong>Indication:</strong> ${study.reason}</p>
                        ${study.timing ? `<p style="color: #0066cc;">⏰ ${study.timing}</p>` : ''}
                        <div class="guideline-cite">
                            <strong>📚 Clinical Guideline:</strong> ${study.guideline}
                        </div>
                    </div>
                `).join('');
            }

            // Clarification
            const clarificationContent = document.getElementById('clarificationContent');
            if (recommendations.clarification.length === 0) {
                clarificationContent.innerHTML = '<div class="alert alert-success">✓ No additional patient information needed at this time.</div>';
            } else {
                clarificationContent.innerHTML = '<p style="margin-bottom: 20px;">The following information should be obtained to refine clinical recommendations:</p>' +
                    recommendations.clarification.map(item => `
                    <div class="recommendation-item">
                        <h4>${item.question}</h4>
                        <p><strong>Why this matters:</strong> ${item.reason}</p>
                        <div style="background: #d4edda; padding: 10px; border-radius: 4px; margin-top: 10px;">
                            <strong>Next step:</strong> ${item.action}
                        </div>
                    </div>
                `).join('');
            }

            // Follow-up
            const followupContent = document.getElementById('followupContent');
            followupContent.innerHTML = recommendations.followup.map(item => `
                <div class="recommendation-item">
                    <h4>${item.action}</h4>
                    <div style="display: grid; grid-template-columns: 150px 1fr; gap: 15px; margin-top: 10px;">
                        <div style="background: #e7f3ff; padding: 10px; border-radius: 6px; text-align: center;">
                            <strong>Timing</strong><br>
                            <span style="font-size: 1.2rem; color: #0066cc;">${item.timing}</span>
                        </div>
                        <div>
                            <strong>Rationale:</strong> ${item.reason}
                        </div>
                    </div>
                </div>
            `).join('');

            // Summary
            const symptoms = [];
            if (patientData.vaginalBleeding) symptoms.push('- Vaginal bleeding');
            if (patientData.headache) symptoms.push('- Headache');
            if (patientData.hypertension) symptoms.push('- Known hypertension or elevated BP');
            if (patientData.decreasedMovement) symptoms.push('- Decreased fetal movement');
            if (patientData.otherSymptoms) symptoms.push(`- ${patientData.otherSymptoms}`);

            let summary = `CLINICAL DECISION SUPPORT SUMMARY
Date: ${new Date().toLocaleString()}

PATIENT INFORMATION:
Patient ID: ${patientData.patientId || 'N/A'}
Age: ${patientData.age} years
Gestational Age: ${patientData.gestationalAge.weeks} weeks ${patientData.gestationalAge.days} days (LMP: ${patientData.lmp})
Gravida/Para: ${patientData.gravida}/${patientData.para}

PRESENTING SYMPTOMS/CONCERNS:
${symptoms.length > 0 ? symptoms.join('\n') : '- No acute symptoms reported'}

`;

            if (recommendations.alerts.length > 0) {
                summary += `⚠️  CLINICAL ALERTS:\n`;
                recommendations.alerts.forEach(alert => {
                    summary += `- ${alert.message}: ${alert.action}\n`;
                });
                summary += '\n';
            }

            if (recommendations.tests.length > 0) {
                summary += `RECOMMENDED LABORATORY TESTS:\n`;
                recommendations.tests.forEach((test, i) => {
                    summary += `${i + 1}. ${test.name}\n`;
                    summary += `   Indication: ${test.reason}\n`;
                    summary += `   Guideline: ${test.guideline}\n`;
                    summary += `   Urgency: ${test.urgency.toUpperCase()}\n`;
                    if (test.timing) summary += `   Timing: ${test.timing}\n`;
                    summary += '\n';
                });
            }

            if (recommendations.imaging.length > 0) {
                summary += `RECOMMENDED IMAGING STUDIES:\n`;
                recommendations.imaging.forEach((study, i) => {
                    summary += `${i + 1}. ${study.name}\n`;
                    summary += `   Indication: ${study.reason}\n`;
                    summary += `   Guideline: ${study.guideline}\n`;
                    if (study.timing) summary += `   ${study.timing}\n`;
                    summary += `   Urgency: ${study.urgency.toUpperCase()}\n\n`;
                });
            }

            if (recommendations.clarification.length > 0) {
                summary += `INFORMATION NEEDED FROM PATIENT:\n`;
                recommendations.clarification.forEach((item, i) => {
                    summary += `${i + 1}. ${item.question}\n`;
                    summary += `   Rationale: ${item.reason}\n`;
                    summary += `   Action: ${item.action}\n\n`;
                });
            }

            if (recommendations.followup.length > 0) {
                summary += `FOLLOW-UP CARE PLAN:\n`;
                recommendations.followup.forEach((item, i) => {
                    summary += `${i + 1}. ${item.action} - ${item.timing}\n`;
                    summary += `   Rationale: ${item.reason}\n\n`;
                });
            }

            summary += `---
Generated by Clinical Decision Support System
This is a clinical decision support tool. All recommendations should be reviewed by the treating physician.`;

            document.getElementById('summaryText').value = summary;
        }

        document.getElementById('patientForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const lmpValue = document.getElementById('lmp').value;
            const gestationalAge = calculateGestationalAge(lmpValue);

            const patientData = {
                patientId: document.getElementById('patientId').value,
                age: parseInt(document.getElementById('age').value),
                lmp: lmpValue,
                gestationalAge: gestationalAge,
                gravida: parseInt(document.getElementById('gravida').value),
                para: parseInt(document.getElementById('para').value),
                vaginalBleeding: document.getElementById('bleeding').checked,
                headache: document.getElementById('headache').checked,
                hypertension: document.getElementById('hypertension').checked,
                decreasedMovement: document.getElementById('decreasedMovement').checked,
                otherSymptoms: document.getElementById('otherSymptoms').value
            };

            const recommendations = generateRecommendations(patientData);
            renderRecommendations(patientData, recommendations);

            document.getElementById('welcomeScreen').classList.add('hidden');
            document.getElementById('resultsScreen').classList.remove('hidden');
        });
    </script>
</body>
</html>