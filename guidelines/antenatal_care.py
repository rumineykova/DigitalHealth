"""
Antenatal Care Schedule - Based on NICE NG201
Structured format for querying pregnancy/maternity guidelines
Includes high-risk pathways and decision trees
"""

ANTENATAL_SCHEDULE = {
    "guideline_info": {
        "name": "NICE NG201 - Antenatal Care",
        "source": "NICE Guidelines",
        "url": "https://www.nice.org.uk/guidance/ng201",
        "last_updated": "2024-08"
    },

    # High-risk conditions and their management pathways
    "high_risk_pathways": {
        "previous_pre_eclampsia": {
            "name": "Previous Pre-eclampsia Pathway",
            "risk_factors": ["previous pre-eclampsia", "pre-eclampsia", "preeclampsia", "hellp", "eclampsia"],
            "management": {
                "medications": [
                    {
                        "drug": "Aspirin 150mg daily",
                        "start": "From 12 weeks gestation",
                        "stop": "Continue until 36 weeks",
                        "checklist": [
                            {"item": "Confirm no contraindications to aspirin", "linked_action": "clinical_assessment"},
                            {"item": "Prescribe aspirin 150mg OD", "linked_action": "prescribe"},
                            {"item": "Advise to take at night", "linked_action": "patient_education"},
                            {"item": "Document in notes", "linked_action": "documentation"}
                        ]
                    }
                ],
                "monitoring": [
                    {
                        "test": "Blood pressure monitoring",
                        "frequency": "Every 2-4 weeks until 32 weeks, then weekly",
                        "checklist": [
                            {"item": "Schedule additional BP appointments", "linked_action": "book_follow_up"},
                            {"item": "Provide BP diary if home monitoring", "linked_action": "patient_education"},
                            {"item": "Set alert threshold: >140/90", "linked_action": "documentation"}
                        ]
                    },
                    {
                        "test": "Urine protein screening",
                        "frequency": "At each appointment",
                        "checklist": [
                            {"item": "Dipstick urine at every visit", "linked_action": "order_test"},
                            {"item": "Send urine PCR if protein detected", "linked_action": "order_test"}
                        ]
                    },
                    {
                        "test": "Pre-eclampsia bloods",
                        "frequency": "If symptoms or signs develop",
                        "checklist": [
                            {"item": "FBC", "linked_action": "order_test"},
                            {"item": "U&E", "linked_action": "order_test"},
                            {"item": "LFTs", "linked_action": "order_test"},
                            {"item": "Uric acid", "linked_action": "order_test"}
                        ]
                    },
                    {
                        "test": "Growth scans",
                        "frequency": "28, 32, 36 weeks",
                        "checklist": [
                            {"item": "Book growth scan at 28 weeks", "linked_action": "order_scan"},
                            {"item": "Book growth scan at 32 weeks", "linked_action": "order_scan"},
                            {"item": "Book growth scan at 36 weeks", "linked_action": "order_scan"}
                        ]
                    }
                ],
                "referrals": [
                    {"to": "Consultant-led antenatal care", "timing": "At booking"},
                    {"to": "Maternal medicine if severe previous disease", "timing": "First trimester"}
                ],
                "warning_signs": [
                    "Severe headache not relieved by paracetamol",
                    "Visual disturbances (flashing lights, blurred vision)",
                    "Severe epigastric or right upper quadrant pain",
                    "Sudden swelling of face, hands, or feet",
                    "Feeling very unwell"
                ],
                "delivery_planning": "Plan delivery by 37-38 weeks if uncomplicated; earlier if features develop"
            },
            "decision_tree": {
                "id": "pre_eclampsia_risk",
                "question": "Pre-eclampsia risk assessment - select severity of previous episode:",
                "branches": [
                    {
                        "condition": "Previous severe/early-onset pre-eclampsia (<34 weeks)",
                        "actions": [
                            "Refer to maternal medicine specialist",
                            "Start aspirin 150mg from 12 weeks",
                            "Uterine artery Doppler at 20-24 weeks",
                            "Serial growth scans from 26 weeks",
                            "Consultant-led care throughout"
                        ],
                        "follow_up": "2-weekly from 24 weeks"
                    },
                    {
                        "condition": "Previous late-onset pre-eclampsia (>34 weeks)",
                        "actions": [
                            "Start aspirin 150mg from 12 weeks",
                            "Additional BP monitoring from 24 weeks",
                            "Growth scans at 28, 32, 36 weeks",
                            "Consultant-led or shared care"
                        ],
                        "follow_up": "3-4 weekly until 28 weeks, then 2-weekly"
                    },
                    {
                        "condition": "Previous HELLP syndrome or eclampsia",
                        "actions": [
                            "Urgent maternal medicine referral",
                            "Start aspirin 150mg from 12 weeks",
                            "Detailed counselling about recurrence risk",
                            "Consider low molecular weight heparin",
                            "Intensive monitoring pathway"
                        ],
                        "follow_up": "Weekly from 24 weeks"
                    }
                ]
            }
        },

        "gestational_diabetes": {
            "name": "Gestational Diabetes Pathway",
            "risk_factors": ["gdm", "gestational diabetes", "previous gdm", "bmi >= 30", "family history diabetes",
                           "south asian", "african caribbean", "middle eastern", "previous macrosomia"],
            "management": {
                "screening": [
                    {
                        "test": "75g Oral Glucose Tolerance Test (GTT)",
                        "timing": "24-28 weeks (or at booking if previous GDM)",
                        "checklist": [
                            {"item": "Book GTT appointment", "linked_action": "order_test"},
                            {"item": "Provide fasting instructions", "linked_action": "patient_education"},
                            {"item": "Review result within 1 week", "linked_action": "review_result"}
                        ]
                    }
                ],
                "if_diagnosed": [
                    {
                        "action": "Refer to joint diabetes antenatal clinic",
                        "checklist": [
                            {"item": "Urgent referral to diabetes team", "linked_action": "referral"},
                            {"item": "Provide blood glucose monitor", "linked_action": "prescribe"},
                            {"item": "Dietary advice", "linked_action": "patient_education"},
                            {"item": "Target: fasting <5.3, 1hr post-meal <7.8", "linked_action": "patient_education"}
                        ]
                    }
                ],
                "monitoring": [
                    {"test": "Serial growth scans", "frequency": "28, 32, 36 weeks"},
                    {"test": "Blood glucose monitoring", "frequency": "4 times daily"},
                    {"test": "HbA1c", "frequency": "At diagnosis if unknown diabetes suspected"}
                ],
                "delivery_planning": "Induction at 40+6 weeks if diet-controlled; 39-40 weeks if on medication"
            },
            "decision_tree": {
                "id": "gdm_screening",
                "question": "GDM risk factors present?",
                "branches": [
                    {
                        "condition": "Previous GDM",
                        "actions": [
                            "Offer early GTT at booking or early pregnancy",
                            "If normal, repeat GTT at 24-28 weeks",
                            "Self-monitoring of blood glucose",
                            "Dietary advice from booking"
                        ],
                        "follow_up": "4-weekly until GTT result"
                    },
                    {
                        "condition": "BMI >= 30 or other risk factors",
                        "actions": [
                            "Book GTT for 24-28 weeks",
                            "Lifestyle and dietary advice",
                            "Weight management support"
                        ],
                        "follow_up": "Routine until GTT"
                    },
                    {
                        "condition": "No risk factors",
                        "actions": [
                            "No GTT required",
                            "Routine antenatal care"
                        ],
                        "follow_up": "Routine"
                    }
                ]
            }
        },

        "high_bmi": {
            "name": "High BMI Pathway (BMI >= 35)",
            "risk_factors": ["bmi >= 35", "bmi > 35", "obese", "obesity", "high bmi"],
            "management": {
                "referrals": [
                    {"to": "Consultant-led care", "timing": "At booking"},
                    {"to": "Anaesthetic review", "timing": "Third trimester"},
                    {"to": "Dietitian", "timing": "First trimester"}
                ],
                "monitoring": [
                    {
                        "test": "GTT screening",
                        "timing": "24-28 weeks",
                        "checklist": [
                            {"item": "Book GTT", "linked_action": "order_test"}
                        ]
                    },
                    {
                        "test": "Growth scans",
                        "timing": "May be technically difficult - serial assessments",
                        "checklist": [
                            {"item": "Book growth scan at 28 weeks", "linked_action": "order_scan"},
                            {"item": "Book growth scan at 34 weeks", "linked_action": "order_scan"},
                            {"item": "Book growth scan at 38 weeks", "linked_action": "order_scan"}
                        ]
                    },
                    {
                        "test": "VTE risk assessment",
                        "timing": "Booking and throughout pregnancy",
                        "checklist": [
                            {"item": "Calculate VTE risk score", "linked_action": "clinical_assessment"},
                            {"item": "Consider prophylactic LMWH if additional risk factors", "linked_action": "prescribe"}
                        ]
                    }
                ],
                "additional_considerations": [
                    "Manual handling assessment",
                    "Appropriate equipment availability",
                    "Active birth position discussion",
                    "Increased risk of: GDM, pre-eclampsia, VTE, caesarean section"
                ]
            },
            "decision_tree": {
                "id": "bmi_pathway",
                "question": "BMI category at booking?",
                "branches": [
                    {
                        "condition": "BMI 30-34.9 (Class I obesity)",
                        "actions": [
                            "Shared care possible",
                            "GTT at 24-28 weeks",
                            "VTE risk assessment",
                            "Dietary advice"
                        ],
                        "follow_up": "Routine with GTT"
                    },
                    {
                        "condition": "BMI 35-39.9 (Class II obesity)",
                        "actions": [
                            "Consultant-led care",
                            "Anaesthetic review in third trimester",
                            "GTT at 24-28 weeks",
                            "Serial growth scans",
                            "Consider thromboprophylaxis"
                        ],
                        "follow_up": "4-weekly"
                    },
                    {
                        "condition": "BMI >= 40 (Class III obesity)",
                        "actions": [
                            "Consultant-led care mandatory",
                            "Early anaesthetic review",
                            "Thromboprophylaxis throughout pregnancy",
                            "Serial growth scans from 28 weeks",
                            "Manual handling assessment",
                            "Discuss place of birth (obstetric unit)"
                        ],
                        "follow_up": "2-4 weekly"
                    }
                ]
            }
        },

        "rh_negative": {
            "name": "Rhesus Negative Pathway",
            "risk_factors": ["rh negative", "rhesus negative", "rh neg", "o negative", "a negative", "b negative", "ab negative"],
            "management": {
                "routine_anti_d": [
                    {
                        "timing": "28 weeks",
                        "dose": "1500 IU anti-D immunoglobulin",
                        "checklist": [
                            {"item": "Check antibody screen result", "linked_action": "review_result"},
                            {"item": "Confirm no anti-D antibodies", "linked_action": "clinical_assessment"},
                            {"item": "Administer anti-D 1500 IU IM", "linked_action": "administer_medication"},
                            {"item": "Record batch number", "linked_action": "documentation"}
                        ]
                    }
                ],
                "sensitising_events": [
                    "Vaginal bleeding",
                    "Abdominal trauma",
                    "External cephalic version",
                    "Amniocentesis/CVS",
                    "Ectopic pregnancy",
                    "Miscarriage",
                    "Termination of pregnancy"
                ],
                "sensitising_event_anti_d": {
                    "timing": "Within 72 hours of sensitising event",
                    "dose": "Minimum 250 IU before 20 weeks; 500 IU after 20 weeks (Kleihauer test)",
                    "checklist": [
                        {"item": "Confirm sensitising event", "linked_action": "clinical_assessment"},
                        {"item": "Check if Kleihauer needed (>20 weeks)", "linked_action": "order_test"},
                        {"item": "Administer appropriate anti-D dose", "linked_action": "administer_medication"},
                        {"item": "Document indication and batch", "linked_action": "documentation"}
                    ]
                },
                "postnatal": {
                    "timing": "Within 72 hours of delivery if baby Rh positive",
                    "checklist": [
                        {"item": "Check baby's blood group", "linked_action": "order_test"},
                        {"item": "Perform Kleihauer test", "linked_action": "order_test"},
                        {"item": "Calculate anti-D dose required", "linked_action": "clinical_assessment"},
                        {"item": "Administer anti-D", "linked_action": "administer_medication"}
                    ]
                }
            },
            "decision_tree": {
                "id": "rh_negative_event",
                "question": "Sensitising event in Rh negative woman?",
                "branches": [
                    {
                        "condition": "Sensitising event before 12 weeks",
                        "actions": [
                            "Anti-D not routinely required for threatened miscarriage <12 weeks unless heavy/repeated bleeding",
                            "Anti-D required for ectopic, molar pregnancy, termination, or instrumentation"
                        ],
                        "follow_up": "As per clinical situation"
                    },
                    {
                        "condition": "Sensitising event 12-20 weeks",
                        "actions": [
                            "Administer 250 IU anti-D within 72 hours",
                            "No Kleihauer test needed"
                        ],
                        "follow_up": "Routine"
                    },
                    {
                        "condition": "Sensitising event > 20 weeks",
                        "actions": [
                            "Administer minimum 500 IU anti-D within 72 hours",
                            "Perform Kleihauer test to check for larger fetomaternal haemorrhage",
                            "Additional anti-D if Kleihauer positive"
                        ],
                        "follow_up": "Routine"
                    }
                ]
            }
        },

        "multiple_pregnancy": {
            "name": "Multiple Pregnancy Pathway",
            "risk_factors": ["twins", "multiple pregnancy", "triplets", "dichorionic", "monochorionic", "dcda", "mcda", "mcma"],
            "management": {
                "scan_schedule": {
                    "DCDA (dichorionic diamniotic)": [
                        {"timing": "Every 4 weeks from 24 weeks", "purpose": "Growth and liquor volume"}
                    ],
                    "MCDA (monochorionic diamniotic)": [
                        {"timing": "Every 2 weeks from 16 weeks", "purpose": "TTTS surveillance, growth, liquor"}
                    ],
                    "MCMA (monochorionic monoamniotic)": [
                        {"timing": "Every 2 weeks from 16 weeks, admission from 26 weeks considered", "purpose": "Cord entanglement risk"}
                    ]
                },
                "referrals": [
                    {"to": "Multiple pregnancy specialist team", "timing": "By 14 weeks"},
                    {"to": "Fetal medicine if monochorionic", "timing": "First trimester"}
                ],
                "delivery_timing": {
                    "DCDA": "37+0 to 37+6 weeks",
                    "MCDA": "36+0 to 36+6 weeks",
                    "MCMA": "32-34 weeks after steroids"
                }
            },
            "decision_tree": {
                "id": "multiple_type",
                "question": "Chorionicity of multiple pregnancy?",
                "branches": [
                    {
                        "condition": "DCDA twins (dichorionic diamniotic)",
                        "actions": [
                            "Growth scans every 4 weeks from 24 weeks",
                            "Consultant-led care",
                            "Plan delivery at 37 weeks",
                            "Discuss mode of delivery"
                        ],
                        "follow_up": "4-weekly scans from 24 weeks"
                    },
                    {
                        "condition": "MCDA twins (monochorionic diamniotic)",
                        "actions": [
                            "Refer to fetal medicine",
                            "Scans every 2 weeks from 16 weeks",
                            "Monitor for TTTS (twin-twin transfusion)",
                            "Plan delivery at 36 weeks",
                            "Consider steroids at 34 weeks"
                        ],
                        "follow_up": "2-weekly scans from 16 weeks"
                    },
                    {
                        "condition": "MCMA twins (monochorionic monoamniotic)",
                        "actions": [
                            "Urgent fetal medicine referral",
                            "2-weekly scans from 16 weeks",
                            "Consider inpatient monitoring from 26-28 weeks",
                            "Plan delivery at 32-34 weeks",
                            "Steroids at 32 weeks"
                        ],
                        "follow_up": "2-weekly, then inpatient"
                    }
                ]
            }
        },

        "anaemia": {
            "name": "Anaemia in Pregnancy Pathway",
            "risk_factors": ["anaemia", "anemia", "low hb", "iron deficiency", "low haemoglobin"],
            "thresholds": {
                "first_trimester": "Hb < 110 g/L",
                "second_third_trimester": "Hb < 105 g/L",
                "postpartum": "Hb < 100 g/L"
            },
            "management": {
                "mild_moderate": {
                    "hb_range": "70-105 g/L",
                    "treatment": [
                        {
                            "action": "Oral iron supplementation",
                            "dose": "Ferrous sulphate 200mg BD or ferrous fumarate 210mg BD",
                            "checklist": [
                                {"item": "Check MCV to confirm iron deficiency", "linked_action": "review_result"},
                                {"item": "Prescribe oral iron", "linked_action": "prescribe"},
                                {"item": "Advise on side effects and absorption", "linked_action": "patient_education"},
                                {"item": "Recheck Hb in 2-4 weeks", "linked_action": "order_test"}
                            ]
                        }
                    ]
                },
                "severe": {
                    "hb_range": "< 70 g/L",
                    "treatment": [
                        {
                            "action": "Consider IV iron or transfusion",
                            "checklist": [
                                {"item": "Urgent haematology advice", "linked_action": "referral"},
                                {"item": "Consider IV iron infusion", "linked_action": "prescribe"},
                                {"item": "Transfusion if symptomatic or Hb < 60", "linked_action": "clinical_decision"},
                                {"item": "Monitor response", "linked_action": "order_test"}
                            ]
                        }
                    ]
                }
            },
            "decision_tree": {
                "id": "anaemia_severity",
                "question": "Haemoglobin level and symptoms?",
                "branches": [
                    {
                        "condition": "Hb 100-109 g/L (mild anaemia)",
                        "actions": [
                            "Start oral iron",
                            "Dietary advice",
                            "Recheck Hb in 2-4 weeks"
                        ],
                        "follow_up": "2-4 weeks"
                    },
                    {
                        "condition": "Hb 70-99 g/L (moderate anaemia)",
                        "actions": [
                            "Start oral iron BD dose",
                            "Consider IV iron if not responding or <34 weeks and Hb <90",
                            "Recheck Hb in 2 weeks"
                        ],
                        "follow_up": "2 weeks"
                    },
                    {
                        "condition": "Hb < 70 g/L (severe anaemia)",
                        "actions": [
                            "Urgent haematology referral",
                            "IV iron or transfusion",
                            "Investigate underlying cause",
                            "Daily Hb monitoring until stable"
                        ],
                        "follow_up": "Daily until stable"
                    },
                    {
                        "condition": "Symptomatic at any Hb level",
                        "actions": [
                            "Assess symptoms (SOB, chest pain, tachycardia)",
                            "Consider transfusion if compromised",
                            "Investigate cause"
                        ],
                        "follow_up": "Immediate assessment"
                    }
                ]
            }
        },

        "reduced_fetal_movements": {
            "name": "Reduced Fetal Movements Pathway",
            "risk_factors": ["reduced movements", "decreased movements", "baby not moving", "fewer kicks", "rfm"],
            "management": {
                "assessment": [
                    {
                        "action": "Immediate CTG monitoring",
                        "checklist": [
                            {"item": "Apply CTG monitor", "linked_action": "clinical_procedure"},
                            {"item": "Monitor for minimum 20 minutes", "linked_action": "clinical_procedure"},
                            {"item": "Assess baseline rate, variability, accelerations", "linked_action": "clinical_assessment"},
                            {"item": "Document interpretation", "linked_action": "documentation"}
                        ]
                    },
                    {
                        "action": "Clinical assessment",
                        "checklist": [
                            {"item": "Measure fundal height", "linked_action": "record_vital"},
                            {"item": "Palpate lie and presentation", "linked_action": "clinical_assessment"},
                            {"item": "Listen to fetal heart", "linked_action": "clinical_procedure"},
                            {"item": "Check maternal BP and urinalysis", "linked_action": "record_vital"}
                        ]
                    }
                ],
                "further_investigation": {
                    "if_ctg_normal": "Reassure but advise to return if concerns persist",
                    "if_ctg_abnormal": "Urgent senior review and consider delivery",
                    "consider_ultrasound": "If fundal height small for dates, previous IUGR, or recurrent RFM"
                }
            },
            "decision_tree": {
                "id": "rfm_assessment",
                "question": "CTG assessment result?",
                "branches": [
                    {
                        "condition": "Normal CTG",
                        "actions": [
                            "Reassure mother",
                            "Advise on normal movement patterns",
                            "Return if movements don't improve or concerns recur",
                            "Document in notes"
                        ],
                        "follow_up": "Return if concerns"
                    },
                    {
                        "condition": "Suspicious CTG",
                        "actions": [
                            "Senior midwife/obstetric review",
                            "Consider ultrasound for liquor and growth",
                            "May need continuous monitoring",
                            "Document clear plan"
                        ],
                        "follow_up": "Same day review"
                    },
                    {
                        "condition": "Pathological CTG",
                        "actions": [
                            "Immediate obstetric review",
                            "Consider urgent delivery",
                            "Inform neonatal team",
                            "Maternal steroid if <34 weeks"
                        ],
                        "follow_up": "Immediate action"
                    },
                    {
                        "condition": "Recurrent RFM (2 or more episodes)",
                        "actions": [
                            "Arrange growth scan",
                            "Review for IUGR",
                            "Consider increased surveillance",
                            "Discuss threshold for delivery"
                        ],
                        "follow_up": "Within 24 hours"
                    }
                ]
            }
        }
    },

    # Appointment schedule by gestation week
    "appointments": {
        "booking": {
            "week": "8-12",
            "name": "Booking Appointment",
            "actions": [
                {
                    "id": "booking_history",
                    "action": "Take medical/obstetric history",
                    "checklist": [
                        {"item": "Previous pregnancies and outcomes", "status": "pending"},
                        {"item": "Medical conditions", "status": "pending"},
                        {"item": "Mental health history", "status": "pending"},
                        {"item": "Family history", "status": "pending"},
                        {"item": "Medications and allergies", "status": "pending"},
                        {"item": "Social circumstances", "status": "pending"}
                    ],
                    "section": "1.1"
                },
                {
                    "id": "booking_bloods",
                    "action": "Order booking bloods",
                    "checklist": [
                        {"item": "FBC", "status": "pending", "linked_action": "order_test"},
                        {"item": "Blood group and Rh status", "status": "pending", "linked_action": "order_test"},
                        {"item": "Antibody screen", "status": "pending", "linked_action": "order_test"},
                        {"item": "HIV screening", "status": "pending", "linked_action": "order_test"},
                        {"item": "Hepatitis B screening", "status": "pending", "linked_action": "order_test"},
                        {"item": "Syphilis screening", "status": "pending", "linked_action": "order_test"},
                        {"item": "Rubella susceptibility", "status": "pending", "linked_action": "order_test"},
                        {"item": "Haemoglobinopathy screen", "status": "pending", "linked_action": "order_test"}
                    ],
                    "section": "1.2"
                },
                {
                    "id": "booking_urine",
                    "action": "Urine tests",
                    "checklist": [
                        {"item": "MSU for culture", "status": "pending", "linked_action": "order_test"},
                        {"item": "Proteinuria screening", "status": "pending", "linked_action": "order_test"}
                    ],
                    "section": "1.2"
                },
                {
                    "id": "booking_bp",
                    "action": "Baseline observations",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "BMI calculation", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Weight", "status": "pending", "linked_action": "record_vital"}
                    ],
                    "section": "1.3"
                },
                {
                    "id": "booking_info",
                    "action": "Provide information",
                    "checklist": [
                        {"item": "Folic acid supplementation", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Vitamin D supplementation", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Diet and lifestyle advice", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Screening test information", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Antenatal classes", "status": "pending", "linked_action": "referral"}
                    ],
                    "section": "1.4"
                }
            ],
            "decision_trees": [
                {
                    "id": "high_risk_assessment",
                    "trigger": "booking_history",
                    "question": "Does patient have any high-risk factors?",
                    "branches": [
                        {
                            "condition": "Previous preterm birth",
                            "actions": ["Refer to preterm birth clinic", "Consider cervical length scan at 16 weeks"],
                            "follow_up": "2 weeks"
                        },
                        {
                            "condition": "Previous pre-eclampsia",
                            "actions": ["Start aspirin 150mg from 12 weeks", "Arrange additional BP monitoring"],
                            "follow_up": "2 weeks"
                        },
                        {
                            "condition": "BMI >= 35",
                            "actions": ["Refer to consultant-led care", "Glucose tolerance test at 24-28 weeks", "Anaesthetic review in third trimester"],
                            "follow_up": "4 weeks"
                        },
                        {
                            "condition": "Diabetes (pre-existing)",
                            "actions": ["Refer to joint diabetes-obstetric clinic", "Retinal screening", "Renal function assessment"],
                            "follow_up": "2 weeks"
                        },
                        {
                            "condition": "No high-risk factors",
                            "actions": ["Continue standard antenatal pathway"],
                            "follow_up": "16 weeks"
                        }
                    ]
                }
            ]
        },

        "week_11_14": {
            "week": "11-14",
            "name": "Dating/Nuchal Scan & Combined Screening",
            "actions": [
                {
                    "id": "dating_scan",
                    "action": "Arrange dating ultrasound",
                    "checklist": [
                        {"item": "Confirm viability", "status": "pending", "linked_action": "order_scan"},
                        {"item": "Confirm dates/EDD", "status": "pending", "linked_action": "record_result"},
                        {"item": "Number of fetuses", "status": "pending", "linked_action": "record_result"},
                        {"item": "Nuchal translucency measurement", "status": "pending", "linked_action": "record_result"}
                    ],
                    "section": "1.5"
                },
                {
                    "id": "combined_screening",
                    "action": "Offer combined screening for Down's, Edwards', Patau's",
                    "checklist": [
                        {"item": "Discuss screening options", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Take blood for PAPP-A and hCG", "status": "pending", "linked_action": "order_test"},
                        {"item": "Document consent/decline", "status": "pending", "linked_action": "documentation"}
                    ],
                    "section": "1.5"
                }
            ],
            "decision_trees": [
                {
                    "id": "screening_result",
                    "trigger": "combined_screening",
                    "question": "Combined screening result?",
                    "branches": [
                        {
                            "condition": "High risk (>=1:150)",
                            "actions": ["Offer diagnostic testing (CVS/amniocentesis)", "Refer to fetal medicine", "Provide written information"],
                            "follow_up": "Within 3 days"
                        },
                        {
                            "condition": "Low risk (<1:150)",
                            "actions": ["Reassure and document", "Continue routine pathway"],
                            "follow_up": "16 weeks"
                        },
                        {
                            "condition": "Declined screening",
                            "actions": ["Document informed decline", "Continue routine pathway"],
                            "follow_up": "16 weeks"
                        }
                    ]
                }
            ]
        },

        "week_16": {
            "week": "16",
            "name": "16-Week Appointment",
            "actions": [
                {
                    "id": "review_results",
                    "action": "Review booking results",
                    "checklist": [
                        {"item": "Check all booking bloods received", "status": "pending", "linked_action": "review_result"},
                        {"item": "Review screening results", "status": "pending", "linked_action": "review_result"},
                        {"item": "Action any abnormal results", "status": "pending", "linked_action": "clinical_action"}
                    ],
                    "section": "1.6"
                },
                {
                    "id": "week16_obs",
                    "action": "Clinical observations",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis for protein", "status": "pending", "linked_action": "order_test"}
                    ],
                    "section": "1.6"
                },
                {
                    "id": "week16_info",
                    "action": "Information giving",
                    "checklist": [
                        {"item": "Anomaly scan information", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Whooping cough vaccination info", "status": "pending", "linked_action": "patient_education"}
                    ],
                    "section": "1.6"
                }
            ],
            "decision_trees": [
                {
                    "id": "anaemia_check",
                    "trigger": "review_results",
                    "question": "Booking Hb result?",
                    "branches": [
                        {
                            "condition": "Hb < 110 g/L",
                            "actions": ["Start iron supplementation", "Recheck Hb in 2-4 weeks", "Consider referral if severe"],
                            "follow_up": "2-4 weeks"
                        },
                        {
                            "condition": "Hb >= 110 g/L",
                            "actions": ["No action required", "Routine recheck at 28 weeks"],
                            "follow_up": "28 weeks"
                        }
                    ]
                },
                {
                    "id": "rh_negative",
                    "trigger": "review_results",
                    "question": "Blood group Rh status?",
                    "branches": [
                        {
                            "condition": "Rh negative",
                            "actions": ["Discuss anti-D prophylaxis", "Arrange anti-D at 28 weeks", "Check for antibodies"],
                            "follow_up": "28 weeks"
                        },
                        {
                            "condition": "Rh positive",
                            "actions": ["No anti-D required"],
                            "follow_up": "Routine"
                        }
                    ]
                }
            ]
        },

        "week_18_22": {
            "week": "18-22",
            "name": "Anomaly Scan",
            "actions": [
                {
                    "id": "anomaly_scan",
                    "action": "Arrange anomaly scan",
                    "checklist": [
                        {"item": "Fetal anomaly survey", "status": "pending", "linked_action": "order_scan"},
                        {"item": "Placental location", "status": "pending", "linked_action": "record_result"},
                        {"item": "Amniotic fluid volume", "status": "pending", "linked_action": "record_result"},
                        {"item": "Fetal biometry", "status": "pending", "linked_action": "record_result"}
                    ],
                    "section": "1.7"
                }
            ],
            "decision_trees": [
                {
                    "id": "anomaly_result",
                    "trigger": "anomaly_scan",
                    "question": "Anomaly scan findings?",
                    "branches": [
                        {
                            "condition": "Anomaly detected",
                            "actions": ["Urgent fetal medicine referral", "Multidisciplinary team discussion", "Provide written information"],
                            "follow_up": "Within 5 days"
                        },
                        {
                            "condition": "Low-lying placenta",
                            "actions": ["Arrange repeat scan at 32 weeks", "Advise to attend if bleeding"],
                            "follow_up": "32 weeks"
                        },
                        {
                            "condition": "Normal scan",
                            "actions": ["Reassure", "Continue routine pathway"],
                            "follow_up": "25 weeks"
                        }
                    ]
                }
            ]
        },

        "week_25": {
            "week": "25",
            "name": "25-Week Appointment (Nulliparous only)",
            "applies_to": "nulliparous",
            "actions": [
                {
                    "id": "week25_obs",
                    "action": "Clinical assessment",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis", "status": "pending", "linked_action": "order_test"},
                        {"item": "Symphysis-fundal height", "status": "pending", "linked_action": "record_vital"}
                    ],
                    "section": "1.8"
                }
            ],
            "decision_trees": []
        },

        "week_28": {
            "week": "28",
            "name": "28-Week Appointment",
            "actions": [
                {
                    "id": "week28_obs",
                    "action": "Clinical assessment",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis", "status": "pending", "linked_action": "order_test"},
                        {"item": "Symphysis-fundal height", "status": "pending", "linked_action": "record_vital"}
                    ],
                    "section": "1.9"
                },
                {
                    "id": "week28_bloods",
                    "action": "28-week blood tests",
                    "checklist": [
                        {"item": "FBC (Hb check)", "status": "pending", "linked_action": "order_test"},
                        {"item": "Antibody screen", "status": "pending", "linked_action": "order_test"}
                    ],
                    "section": "1.9"
                },
                {
                    "id": "anti_d",
                    "action": "Anti-D if Rh negative",
                    "checklist": [
                        {"item": "Administer anti-D 1500 IU", "status": "pending", "linked_action": "administer_medication"}
                    ],
                    "section": "1.9",
                    "condition": "Rh negative"
                },
                {
                    "id": "whooping_cough",
                    "action": "Pertussis vaccination",
                    "checklist": [
                        {"item": "Offer whooping cough vaccine", "status": "pending", "linked_action": "administer_vaccination"},
                        {"item": "Document consent/administration", "status": "pending", "linked_action": "documentation"}
                    ],
                    "section": "1.9"
                }
            ],
            "decision_trees": [
                {
                    "id": "gtt_screening",
                    "trigger": "risk_factors",
                    "question": "GDM risk factors present?",
                    "branches": [
                        {
                            "condition": "BMI >= 30, previous GDM, family history DM, high-risk ethnicity",
                            "actions": ["Arrange GTT at 24-28 weeks", "Dietary advice"],
                            "follow_up": "Depends on GTT result"
                        },
                        {
                            "condition": "No risk factors",
                            "actions": ["No GTT required"],
                            "follow_up": "Routine"
                        }
                    ]
                },
                {
                    "id": "anaemia_28",
                    "trigger": "week28_bloods",
                    "question": "28-week Hb result?",
                    "branches": [
                        {
                            "condition": "Hb < 105 g/L",
                            "actions": ["Start/increase iron", "Dietary advice", "Recheck in 2-4 weeks"],
                            "follow_up": "2-4 weeks"
                        },
                        {
                            "condition": "Hb >= 105 g/L",
                            "actions": ["No action"],
                            "follow_up": "Routine"
                        }
                    ]
                }
            ]
        },

        "week_31": {
            "week": "31",
            "name": "31-Week Appointment (Nulliparous only)",
            "applies_to": "nulliparous",
            "actions": [
                {
                    "id": "week31_obs",
                    "action": "Clinical assessment",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis", "status": "pending", "linked_action": "order_test"},
                        {"item": "Symphysis-fundal height", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Review 28-week blood results", "status": "pending", "linked_action": "review_result"}
                    ],
                    "section": "1.10"
                }
            ],
            "decision_trees": []
        },

        "week_34": {
            "week": "34",
            "name": "34-Week Appointment",
            "actions": [
                {
                    "id": "week34_obs",
                    "action": "Clinical assessment",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis", "status": "pending", "linked_action": "order_test"},
                        {"item": "Symphysis-fundal height", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Fetal presentation", "status": "pending", "linked_action": "record_result"}
                    ],
                    "section": "1.11"
                },
                {
                    "id": "week34_info",
                    "action": "Information giving",
                    "checklist": [
                        {"item": "Birth plan discussion", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Labour signs information", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Breastfeeding information", "status": "pending", "linked_action": "patient_education"}
                    ],
                    "section": "1.11"
                },
                {
                    "id": "second_anti_d",
                    "action": "Second anti-D if required",
                    "checklist": [
                        {"item": "Administer anti-D if two-dose regimen", "status": "pending", "linked_action": "administer_medication"}
                    ],
                    "section": "1.11",
                    "condition": "Rh negative, two-dose regimen"
                }
            ],
            "decision_trees": [
                {
                    "id": "presentation_34",
                    "trigger": "week34_obs",
                    "question": "Fetal presentation at 34 weeks?",
                    "branches": [
                        {
                            "condition": "Breech",
                            "actions": ["Confirm with ultrasound", "Discuss ECV at 36-37 weeks", "Provide information leaflet"],
                            "follow_up": "36 weeks"
                        },
                        {
                            "condition": "Cephalic",
                            "actions": ["Reassure", "Continue routine pathway"],
                            "follow_up": "36 weeks"
                        },
                        {
                            "condition": "Uncertain",
                            "actions": ["Arrange presentation scan"],
                            "follow_up": "Within 1 week"
                        }
                    ]
                }
            ]
        },

        "week_36": {
            "week": "36",
            "name": "36-Week Appointment",
            "actions": [
                {
                    "id": "week36_obs",
                    "action": "Clinical assessment",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis", "status": "pending", "linked_action": "order_test"},
                        {"item": "Symphysis-fundal height", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Fetal presentation", "status": "pending", "linked_action": "record_result"}
                    ],
                    "section": "1.12"
                },
                {
                    "id": "week36_info",
                    "action": "Information and planning",
                    "checklist": [
                        {"item": "Birth options discussion", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Postdates management discussion", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Pain relief options", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Vitamin K discussion", "status": "pending", "linked_action": "patient_education"}
                    ],
                    "section": "1.12"
                }
            ],
            "decision_trees": [
                {
                    "id": "ecv_decision",
                    "trigger": "week36_obs",
                    "question": "Breech presentation at 36 weeks?",
                    "branches": [
                        {
                            "condition": "Confirmed breech, ECV accepted",
                            "actions": ["Book ECV at 36-37 weeks", "Pre-ECV bloods (FBC, group & save)", "Consent for procedure"],
                            "follow_up": "ECV appointment"
                        },
                        {
                            "condition": "Confirmed breech, ECV declined",
                            "actions": ["Discuss birth options (vaginal breech vs caesarean)", "Consultant review", "Birth plan"],
                            "follow_up": "38 weeks"
                        },
                        {
                            "condition": "Cephalic",
                            "actions": ["Continue routine pathway"],
                            "follow_up": "38 weeks"
                        }
                    ]
                }
            ]
        },

        "week_38": {
            "week": "38",
            "name": "38-Week Appointment",
            "actions": [
                {
                    "id": "week38_obs",
                    "action": "Clinical assessment",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis", "status": "pending", "linked_action": "order_test"},
                        {"item": "Symphysis-fundal height", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Fetal presentation", "status": "pending", "linked_action": "record_result"}
                    ],
                    "section": "1.13"
                },
                {
                    "id": "week38_plan",
                    "action": "Birth planning",
                    "checklist": [
                        {"item": "Finalize birth plan", "status": "pending", "linked_action": "documentation"},
                        {"item": "Discuss membrane sweep offer at 40/41 weeks", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Postdates induction discussion", "status": "pending", "linked_action": "patient_education"}
                    ],
                    "section": "1.13"
                }
            ],
            "decision_trees": []
        },

        "week_40": {
            "week": "40",
            "name": "40-Week Appointment (Nulliparous only)",
            "applies_to": "nulliparous",
            "actions": [
                {
                    "id": "week40_obs",
                    "action": "Clinical assessment",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis", "status": "pending", "linked_action": "order_test"},
                        {"item": "Symphysis-fundal height", "status": "pending", "linked_action": "record_vital"}
                    ],
                    "section": "1.14"
                },
                {
                    "id": "membrane_sweep",
                    "action": "Offer membrane sweep",
                    "checklist": [
                        {"item": "Discuss membrane sweep", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Perform if accepted", "status": "pending", "linked_action": "clinical_procedure"},
                        {"item": "Document findings/outcome", "status": "pending", "linked_action": "documentation"}
                    ],
                    "section": "1.14"
                }
            ],
            "decision_trees": []
        },

        "week_41": {
            "week": "41",
            "name": "41-Week Appointment",
            "actions": [
                {
                    "id": "week41_obs",
                    "action": "Clinical assessment",
                    "checklist": [
                        {"item": "Blood pressure", "status": "pending", "linked_action": "record_vital"},
                        {"item": "Urinalysis", "status": "pending", "linked_action": "order_test"},
                        {"item": "Symphysis-fundal height", "status": "pending", "linked_action": "record_vital"}
                    ],
                    "section": "1.15"
                },
                {
                    "id": "postdates_plan",
                    "action": "Postdates management",
                    "checklist": [
                        {"item": "Offer membrane sweep", "status": "pending", "linked_action": "clinical_procedure"},
                        {"item": "Discuss induction of labour", "status": "pending", "linked_action": "patient_education"},
                        {"item": "Book IOL if accepted", "status": "pending", "linked_action": "book_procedure"},
                        {"item": "Discuss expectant management risks", "status": "pending", "linked_action": "patient_education"}
                    ],
                    "section": "1.15"
                }
            ],
            "decision_trees": [
                {
                    "id": "postdates_decision",
                    "trigger": "postdates_plan",
                    "question": "Patient decision on postdates management?",
                    "branches": [
                        {
                            "condition": "Accepts IOL",
                            "actions": ["Book IOL between 41+0 and 42+0 weeks", "Explain IOL process", "Provide written information"],
                            "follow_up": "IOL date"
                        },
                        {
                            "condition": "Declines IOL - expectant management",
                            "actions": ["Twice-weekly CTG and AFI monitoring", "Daily fetal movement awareness", "Review at 42 weeks"],
                            "follow_up": "3-4 days"
                        }
                    ]
                }
            ]
        }
    },

    # Red flags that require immediate action
    "red_flags": [
        {
            "condition": "Vaginal bleeding",
            "keywords": ["bleeding", "bleed", "blood", "spotting", "haemorrhage"],
            "message": "URGENT: Vaginal bleeding in pregnancy - immediate assessment required",
            "actions": ["Urgent assessment", "Speculum examination", "Ultrasound", "Anti-D if Rh negative"]
        },
        {
            "condition": "Reduced fetal movements",
            "keywords": ["reduced movements", "decreased movements", "baby not moving", "fewer kicks", "rfm", "less movement"],
            "message": "URGENT: Reduced fetal movements - same-day assessment",
            "actions": ["CTG monitoring", "Ultrasound if indicated", "Document fetal movements"]
        },
        {
            "condition": "BP >= 140/90",
            "keywords": ["high bp", "elevated bp", "raised bp", "hypertension"],
            "message": "WARNING: Elevated blood pressure - pre-eclampsia screening required",
            "actions": ["Repeat BP", "Urinalysis for proteinuria", "Bloods: FBC, U&E, LFTs", "Consider fetal monitoring"]
        },
        {
            "condition": "Proteinuria >= 1+",
            "keywords": ["protein in urine", "proteinuria"],
            "message": "WARNING: Proteinuria detected - assess for pre-eclampsia",
            "actions": ["Send urine PCR", "Check BP", "Review symptoms", "Consider day unit assessment"]
        },
        {
            "condition": "Severe headache or visual disturbance",
            "keywords": ["headache", "visual", "flashing", "blurred vision", "see spots"],
            "message": "URGENT: Possible pre-eclampsia - immediate assessment",
            "actions": ["Check BP urgently", "Full pre-eclampsia bloods", "Consider admission"]
        },
        {
            "condition": "Abdominal pain",
            "keywords": ["abdominal pain", "tummy pain", "stomach pain", "cramping", "contractions"],
            "message": "URGENT: Abdominal pain requires assessment",
            "actions": ["Assess for placental abruption", "CTG if viable gestation", "Urgent ultrasound if indicated"]
        },
        {
            "condition": "Rupture of membranes < 37 weeks",
            "keywords": ["waters broken", "waters broke", "leaking fluid", "membranes ruptured", "pprom", "prom"],
            "message": "URGENT: Preterm prelabour rupture of membranes",
            "actions": ["Admit to hospital", "Speculum examination", "High vaginal swab", "Consider steroids and antibiotics"]
        },
        {
            "condition": "Regular contractions < 37 weeks",
            "keywords": ["contractions", "preterm labour", "premature labour"],
            "message": "URGENT: Possible preterm labour",
            "actions": ["Assess cervical change", "Consider tocolysis", "Steroids if 24-34 weeks", "Magnesium sulphate if <30 weeks"]
        }
    ],

    # Linked action types and their workflows
    "action_types": {
        "order_test": {
            "name": "Order Test",
            "workflow": ["Select test", "Generate order", "Confirm sent", "Await result"],
            "status_options": ["ordered", "sample_collected", "processing", "resulted", "reviewed"]
        },
        "order_scan": {
            "name": "Order Scan",
            "workflow": ["Request scan", "Appointment booked", "Scan completed", "Report reviewed"],
            "status_options": ["requested", "booked", "completed", "reported", "reviewed"]
        },
        "record_vital": {
            "name": "Record Vital Sign",
            "workflow": ["Measure", "Record", "Flag if abnormal"],
            "status_options": ["pending", "recorded", "flagged", "reviewed"]
        },
        "record_result": {
            "name": "Record Result",
            "workflow": ["Receive result", "Document", "Action if needed"],
            "status_options": ["awaited", "received", "documented", "actioned"]
        },
        "review_result": {
            "name": "Review Result",
            "workflow": ["Open result", "Interpret", "Document review", "Action"],
            "status_options": ["pending_review", "reviewed", "actioned"]
        },
        "patient_education": {
            "name": "Patient Education",
            "workflow": ["Provide information", "Check understanding", "Document"],
            "status_options": ["pending", "discussed", "leaflet_given", "documented"]
        },
        "referral": {
            "name": "Make Referral",
            "workflow": ["Generate referral", "Send", "Confirm receipt", "Appointment received"],
            "status_options": ["pending", "sent", "acknowledged", "appointment_booked", "seen"]
        },
        "prescribe": {
            "name": "Prescribe Medication",
            "workflow": ["Check allergies", "Select medication", "Write prescription", "Dispense"],
            "status_options": ["pending", "prescribed", "dispensed", "patient_counselled"]
        },
        "administer_medication": {
            "name": "Administer Medication",
            "workflow": ["Check allergies", "Prepare", "Administer", "Document"],
            "status_options": ["pending", "prepared", "administered", "documented"]
        },
        "administer_vaccination": {
            "name": "Administer Vaccination",
            "workflow": ["Check contraindications", "Consent", "Administer", "Document batch"],
            "status_options": ["pending", "consented", "administered", "batch_recorded"]
        },
        "clinical_procedure": {
            "name": "Clinical Procedure",
            "workflow": ["Explain procedure", "Consent", "Perform", "Document findings"],
            "status_options": ["pending", "consented", "performed", "documented"]
        },
        "clinical_assessment": {
            "name": "Clinical Assessment",
            "workflow": ["Assess", "Document findings", "Make plan"],
            "status_options": ["pending", "assessed", "documented"]
        },
        "clinical_decision": {
            "name": "Clinical Decision",
            "workflow": ["Review information", "Make decision", "Document rationale"],
            "status_options": ["pending", "decided", "documented"]
        },
        "book_follow_up": {
            "name": "Book Follow-up",
            "workflow": ["Check availability", "Book appointment", "Confirm with patient"],
            "status_options": ["pending", "booked", "confirmed"]
        },
        "book_procedure": {
            "name": "Book Procedure",
            "workflow": ["Check availability", "Book slot", "Confirm with patient", "Send details"],
            "status_options": ["pending", "booked", "confirmed", "patient_notified"]
        },
        "documentation": {
            "name": "Documentation",
            "workflow": ["Document in notes"],
            "status_options": ["pending", "documented"]
        },
        "clinical_action": {
            "name": "Clinical Action Required",
            "workflow": ["Review finding", "Determine action", "Execute", "Document"],
            "status_options": ["pending", "reviewed", "actioned", "documented"]
        }
    }
}


def get_appointment_by_week(gestation_weeks: int) -> dict:
    """Get the appropriate appointment based on gestation"""
    appointments = ANTENATAL_SCHEDULE["appointments"]

    if gestation_weeks <= 12:
        return appointments.get("booking")
    elif 11 <= gestation_weeks <= 14:
        return appointments.get("week_11_14")
    elif 14 < gestation_weeks <= 17:
        return appointments.get("week_16")
    elif 18 <= gestation_weeks <= 22:
        return appointments.get("week_18_22")
    elif 23 <= gestation_weeks <= 27:
        return appointments.get("week_25")
    elif 28 <= gestation_weeks <= 30:
        return appointments.get("week_28")
    elif 31 <= gestation_weeks <= 33:
        return appointments.get("week_31")
    elif 34 <= gestation_weeks <= 35:
        return appointments.get("week_34")
    elif 36 <= gestation_weeks <= 37:
        return appointments.get("week_36")
    elif 38 <= gestation_weeks <= 39:
        return appointments.get("week_38")
    elif gestation_weeks == 40:
        return appointments.get("week_40")
    elif gestation_weeks >= 41:
        return appointments.get("week_41")

    return None


def get_all_appointments_up_to(gestation_weeks: int) -> list:
    """Get all appointments that should have occurred by this gestation"""
    all_appts = []
    week_keys = ["booking", "week_11_14", "week_16", "week_18_22", "week_25",
                 "week_28", "week_31", "week_34", "week_36", "week_38", "week_40", "week_41"]

    week_map = {
        "booking": 12, "week_11_14": 14, "week_16": 16, "week_18_22": 22,
        "week_25": 25, "week_28": 28, "week_31": 31, "week_34": 34,
        "week_36": 36, "week_38": 38, "week_40": 40, "week_41": 41
    }

    for key in week_keys:
        if week_map[key] <= gestation_weeks:
            appt = ANTENATAL_SCHEDULE["appointments"].get(key)
            if appt:
                all_appts.append(appt)

    return all_appts


def check_antenatal_red_flags(symptoms: list, vitals: dict, text_input: str = "") -> list:
    """Check for red flags in antenatal care"""
    alerts = []

    # Combine all text to search
    search_text = " ".join(symptoms).lower() + " " + text_input.lower()

    for flag in ANTENATAL_SCHEDULE["red_flags"]:
        # Check keywords
        keywords = flag.get("keywords", [])
        if any(keyword in search_text for keyword in keywords):
            alerts.append(flag)
            continue

        # Check BP
        if "bp" in flag["condition"].lower() and "BP" in vitals:
            bp = vitals["BP"]
            if "/" in str(bp):
                systolic, diastolic = map(int, str(bp).split("/"))
                if systolic >= 140 or diastolic >= 90:
                    alerts.append(flag)

    return alerts


def get_high_risk_pathway(risk_factors: list, text_input: str = "") -> list:
    """Get applicable high-risk pathways based on risk factors"""
    applicable_pathways = []

    # Combine risk factors and text input for searching
    search_text = " ".join(risk_factors).lower() + " " + text_input.lower()

    for pathway_id, pathway in ANTENATAL_SCHEDULE["high_risk_pathways"].items():
        pathway_triggers = pathway.get("risk_factors", [])
        if any(trigger in search_text for trigger in pathway_triggers):
            applicable_pathways.append((pathway_id, pathway))

    return applicable_pathways


def get_high_risk_recommendations(pathway: dict, gestation_weeks: int) -> dict:
    """Get specific recommendations from a high-risk pathway"""
    recommendations = {
        "name": pathway["name"],
        "medications": [],
        "monitoring": [],
        "referrals": [],
        "warning_signs": [],
        "decision_tree": None
    }

    management = pathway.get("management", {})

    # Get medications
    recommendations["medications"] = management.get("medications", [])

    # Get monitoring requirements
    recommendations["monitoring"] = management.get("monitoring", management.get("screening", []))

    # Get referrals
    recommendations["referrals"] = management.get("referrals", [])

    # Get warning signs
    recommendations["warning_signs"] = management.get("warning_signs", [])

    # Get decision tree
    recommendations["decision_tree"] = pathway.get("decision_tree")

    # Add delivery planning if available
    if "delivery_planning" in management:
        recommendations["delivery_planning"] = management["delivery_planning"]

    return recommendations
