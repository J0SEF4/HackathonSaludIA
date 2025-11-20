from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime, timedelta
import os

app = FastAPI(title="Cardiovascular Health Monitoring API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to CSV data
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "patients_data.csv")

def load_patient_data():
    """Load patient data from CSV"""
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Patient data file not found")

def calculate_priority_score(row):
    """
    Calculate cardiovascular priority score based on clinical parameters and risk factors.
    Score ranges from 0-100, higher means higher priority.
    """
    score = 0
    
    # Age factor (0-15 points)
    age = row['age']
    if age >= 75:
        score += 15
    elif age >= 65:
        score += 10
    elif age >= 55:
        score += 5
    
    # Blood pressure (0-20 points)
    systolic = row['systolic_bp']
    diastolic = row['diastolic_bp']
    if systolic >= 160 or diastolic >= 100:
        score += 20
    elif systolic >= 140 or diastolic >= 90:
        score += 12
    elif systolic >= 130 or diastolic >= 80:
        score += 5
    
    # Cholesterol (0-15 points)
    cholesterol = row['cholesterol']
    ldl = row['ldl']
    if cholesterol >= 240 or ldl >= 160:
        score += 15
    elif cholesterol >= 200 or ldl >= 130:
        score += 10
    elif cholesterol >= 180 or ldl >= 100:
        score += 5
    
    # Glucose (0-15 points)
    glucose = row['glucose']
    if glucose >= 200:
        score += 15
    elif glucose >= 140:
        score += 10
    elif glucose >= 100:
        score += 5
    
    # BMI (0-10 points)
    bmi = row['bmi']
    if bmi >= 35:
        score += 10
    elif bmi >= 30:
        score += 6
    elif bmi >= 25:
        score += 3
    
    # Risk factors (0-25 points)
    if row['diabetes'] == 'Yes':
        score += 10
    if row['hypertension'] == 'Yes':
        score += 8
    if row['smoker'] == 'Yes':
        score += 7
    
    # Previous events (0-15 points)
    if row['previous_mi'] == 'Yes':
        score += 10
    if row['previous_stroke'] == 'Yes':
        score += 10
    
    # Medication compliance (0-10 points penalty for poor compliance)
    if row['medication_compliance'] == 'Low':
        score += 10
    elif row['medication_compliance'] == 'Medium':
        score += 5
    
    # Cap at 100
    return min(score, 100)

def days_since_date(date_str):
    """Calculate days since a given date"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - date).days
    except:
        return 0

def is_lost_patient(row):
    """
    Determine if a patient is "lost" based on:
    - No control visit in >180 days
    - No medication pickup in >90 days
    - Missing exams (>365 days since last exam)
    """
    days_since_control = days_since_date(row['last_control'])
    days_since_medication = days_since_date(row['last_medication'])
    days_since_exam = days_since_date(row['last_exam'])
    
    lost_reasons = []
    
    if days_since_control > 180:
        lost_reasons.append(f"No control visit in {days_since_control} days")
    
    if days_since_medication > 90:
        lost_reasons.append(f"No medication pickup in {days_since_medication} days")
    
    if days_since_exam > 365:
        lost_reasons.append(f"Missing exams ({days_since_exam} days)")
    
    return len(lost_reasons) > 0, lost_reasons

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cardiovascular Health Monitoring API",
        "endpoints": {
            "/priority": "Get priority-sorted patients with cardiovascular risk scores",
            "/lost": "Get list of lost patients",
            "/audit": "Get audit KPIs"
        }
    }

@app.get("/priority")
async def get_priority_patients(limit: Optional[int] = None):
    """
    Calculate and return patients sorted by cardiovascular priority score.
    Higher scores indicate higher priority for intervention.
    """
    df = load_patient_data()
    
    # Calculate priority score for each patient
    df['priority_score'] = df.apply(calculate_priority_score, axis=1)
    
    # Sort by priority score (highest first)
    df_sorted = df.sort_values('priority_score', ascending=False)
    
    # Select relevant columns
    result_df = df_sorted[[
        'patient_id', 'name', 'age', 'gender',
        'systolic_bp', 'diastolic_bp', 'cholesterol', 'glucose',
        'diabetes', 'hypertension', 'smoker',
        'medication_compliance', 'priority_score'
    ]]
    
    if limit:
        result_df = result_df.head(limit)
    
    patients = result_df.to_dict('records')
    
    return {
        "total_patients": len(patients),
        "patients": patients,
        "score_info": {
            "max_score": 100,
            "description": "Higher scores indicate higher cardiovascular risk and priority for intervention"
        }
    }

@app.get("/lost")
async def get_lost_patients():
    """
    Identify and return patients who are "lost" based on:
    - No control visit in >180 days
    - No medication pickup in >90 days
    - Missing exams (>365 days since last exam)
    """
    df = load_patient_data()
    
    lost_patients = []
    
    for _, row in df.iterrows():
        is_lost, reasons = is_lost_patient(row)
        
        if is_lost:
            lost_patients.append({
                "patient_id": row['patient_id'],
                "name": row['name'],
                "age": row['age'],
                "last_control": row['last_control'],
                "last_medication": row['last_medication'],
                "last_exam": row['last_exam'],
                "days_since_control": days_since_date(row['last_control']),
                "days_since_medication": days_since_date(row['last_medication']),
                "days_since_exam": days_since_date(row['last_exam']),
                "lost_reasons": reasons,
                "risk_factors": {
                    "diabetes": row['diabetes'],
                    "hypertension": row['hypertension'],
                    "smoker": row['smoker']
                }
            })
    
    # Sort by number of reasons (most critical first)
    lost_patients.sort(key=lambda x: len(x['lost_reasons']), reverse=True)
    
    return {
        "total_lost": len(lost_patients),
        "patients": lost_patients,
        "thresholds": {
            "control_visit": "180 days",
            "medication_pickup": "90 days",
            "exam": "365 days"
        }
    }

@app.get("/audit")
async def get_audit_kpis():
    """
    Generate audit KPIs for cardiovascular health program:
    - Total patients
    - High risk patients (score > 70)
    - Lost patients count and percentage
    - Control compliance
    - Medication compliance
    - Exam compliance
    - Average risk score
    """
    df = load_patient_data()
    
    # Calculate priority scores
    df['priority_score'] = df.apply(calculate_priority_score, axis=1)
    
    # Calculate lost patients
    lost_count = 0
    control_compliant = 0
    medication_compliant = 0
    exam_compliant = 0
    
    for _, row in df.iterrows():
        is_lost, _ = is_lost_patient(row)
        if is_lost:
            lost_count += 1
        
        # Compliance checks
        if days_since_date(row['last_control']) <= 180:
            control_compliant += 1
        
        if days_since_date(row['last_medication']) <= 90:
            medication_compliant += 1
        
        if days_since_date(row['last_exam']) <= 365:
            exam_compliant += 1
    
    total_patients = len(df)
    high_risk_count = len(df[df['priority_score'] > 70])
    
    # Risk factor distribution
    diabetes_count = len(df[df['diabetes'] == 'Yes'])
    hypertension_count = len(df[df['hypertension'] == 'Yes'])
    smoker_count = len(df[df['smoker'] == 'Yes'])
    
    # Previous events
    previous_mi_count = len(df[df['previous_mi'] == 'Yes'])
    previous_stroke_count = len(df[df['previous_stroke'] == 'Yes'])
    
    return {
        "total_patients": total_patients,
        "high_risk_patients": {
            "count": high_risk_count,
            "percentage": round((high_risk_count / total_patients) * 100, 1)
        },
        "lost_patients": {
            "count": lost_count,
            "percentage": round((lost_count / total_patients) * 100, 1)
        },
        "compliance": {
            "control_visits": {
                "compliant": control_compliant,
                "percentage": round((control_compliant / total_patients) * 100, 1)
            },
            "medication_pickup": {
                "compliant": medication_compliant,
                "percentage": round((medication_compliant / total_patients) * 100, 1)
            },
            "exams": {
                "compliant": exam_compliant,
                "percentage": round((exam_compliant / total_patients) * 100, 1)
            }
        },
        "risk_factors": {
            "diabetes": {
                "count": diabetes_count,
                "percentage": round((diabetes_count / total_patients) * 100, 1)
            },
            "hypertension": {
                "count": hypertension_count,
                "percentage": round((hypertension_count / total_patients) * 100, 1)
            },
            "smokers": {
                "count": smoker_count,
                "percentage": round((smoker_count / total_patients) * 100, 1)
            }
        },
        "previous_events": {
            "myocardial_infarction": {
                "count": previous_mi_count,
                "percentage": round((previous_mi_count / total_patients) * 100, 1)
            },
            "stroke": {
                "count": previous_stroke_count,
                "percentage": round((previous_stroke_count / total_patients) * 100, 1)
            }
        },
        "average_risk_score": round(df['priority_score'].mean(), 1),
        "score_distribution": {
            "low_risk": len(df[df['priority_score'] < 40]),
            "medium_risk": len(df[(df['priority_score'] >= 40) & (df['priority_score'] <= 70)]),
            "high_risk": len(df[df['priority_score'] > 70])
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
