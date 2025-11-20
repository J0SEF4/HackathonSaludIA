from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime, timedelta
import os

app = FastAPI(title="API de Monitoreo de Salud Cardiovascular")

# Middleware CORS para frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta al archivo CSV de datos
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "patients_data.csv")

def load_patient_data():
    """Cargar datos de pacientes desde CSV"""
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de datos de pacientes no encontrado")

def calculate_priority_score(row):
    """
    Calcular puntaje de prioridad cardiovascular basado en parámetros clínicos y factores de riesgo.
    El puntaje varía de 0-100, mayor puntaje significa mayor prioridad.
    """
    score = 0
    
    # Factor edad (0-15 puntos)
    age = row['age']
    if age >= 75:
        score += 15
    elif age >= 65:
        score += 10
    elif age >= 55:
        score += 5
    
    # Presión arterial (0-20 puntos)
    systolic = row['systolic_bp']
    diastolic = row['diastolic_bp']
    if systolic >= 160 or diastolic >= 100:
        score += 20
    elif systolic >= 140 or diastolic >= 90:
        score += 12
    elif systolic >= 130 or diastolic >= 80:
        score += 5
    
    # Colesterol (0-15 puntos)
    cholesterol = row['cholesterol']
    ldl = row['ldl']
    if cholesterol >= 240 or ldl >= 160:
        score += 15
    elif cholesterol >= 200 or ldl >= 130:
        score += 10
    elif cholesterol >= 180 or ldl >= 100:
        score += 5
    
    # Glucosa (0-15 puntos)
    glucose = row['glucose']
    if glucose >= 200:
        score += 15
    elif glucose >= 140:
        score += 10
    elif glucose >= 100:
        score += 5
    
    # IMC (0-10 puntos)
    bmi = row['bmi']
    if bmi >= 35:
        score += 10
    elif bmi >= 30:
        score += 6
    elif bmi >= 25:
        score += 3
    
    # Factores de riesgo (0-25 puntos)
    if row['diabetes'] == 'Yes':
        score += 10
    if row['hypertension'] == 'Yes':
        score += 8
    if row['smoker'] == 'Yes':
        score += 7
    
    # Eventos previos (0-15 puntos)
    if row['previous_mi'] == 'Yes':
        score += 10
    if row['previous_stroke'] == 'Yes':
        score += 10
    
    # Adherencia a medicamentos (0-10 puntos de penalización por baja adherencia)
    if row['medication_compliance'] == 'Low':
        score += 10
    elif row['medication_compliance'] == 'Medium':
        score += 5
    
    # Límite máximo de 100
    return min(score, 100)

def days_since_date(date_str):
    """Calcular días desde una fecha dada"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - date).days
    except:
        return 0

def is_lost_patient(row):
    """
    Determinar si un paciente está "perdido" basado en:
    - Sin visita de control en >180 días
    - Sin retiro de medicamentos en >90 días
    - Exámenes pendientes (>365 días desde el último examen)
    """
    days_since_control = days_since_date(row['last_control'])
    days_since_medication = days_since_date(row['last_medication'])
    days_since_exam = days_since_date(row['last_exam'])
    
    lost_reasons = []
    
    if days_since_control > 180:
        lost_reasons.append(f"Sin visita de control en {days_since_control} días")
    
    if days_since_medication > 90:
        lost_reasons.append(f"Sin retiro de medicamentos en {days_since_medication} días")
    
    if days_since_exam > 365:
        lost_reasons.append(f"Exámenes pendientes ({days_since_exam} días)")
    
    return len(lost_reasons) > 0, lost_reasons

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de Monitoreo de Salud Cardiovascular",
        "endpoints": {
            "/priority": "Obtener pacientes ordenados por prioridad con puntajes de riesgo cardiovascular",
            "/lost": "Obtener lista de pacientes perdidos",
            "/audit": "Obtener KPIs de auditoría"
        }
    }

@app.get("/priority")
async def get_priority_patients(limit: Optional[int] = None):
    """
    Calcular y retornar pacientes ordenados por puntaje de prioridad cardiovascular.
    Puntajes más altos indican mayor prioridad para intervención.
    """
    df = load_patient_data()
    
    # Calcular puntaje de prioridad para cada paciente
    df['priority_score'] = df.apply(calculate_priority_score, axis=1)
    
    # Ordenar por puntaje de prioridad (mayor primero)
    df_sorted = df.sort_values('priority_score', ascending=False)
    
    # Seleccionar columnas relevantes
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
            "description": "Puntajes más altos indican mayor riesgo cardiovascular y prioridad para intervención"
        }
    }

@app.get("/lost")
async def get_lost_patients():
    """
    Identificar y retornar pacientes que están "perdidos" basado en:
    - Sin visita de control en >180 días
    - Sin retiro de medicamentos en >90 días
    - Exámenes pendientes (>365 días desde el último examen)
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
    
    # Ordenar por número de razones (más críticos primero)
    lost_patients.sort(key=lambda x: len(x['lost_reasons']), reverse=True)
    
    return {
        "total_lost": len(lost_patients),
        "patients": lost_patients,
        "thresholds": {
            "control_visit": "180 días",
            "medication_pickup": "90 días",
            "exam": "365 días"
        }
    }

@app.get("/audit")
async def get_audit_kpis():
    """
    Generar KPIs de auditoría para programa de salud cardiovascular:
    - Total de pacientes
    - Pacientes de alto riesgo (puntaje > 70)
    - Cantidad y porcentaje de pacientes perdidos
    - Cumplimiento de controles
    - Cumplimiento de medicamentos
    - Cumplimiento de exámenes
    - Puntaje promedio de riesgo
    """
    df = load_patient_data()
    
    # Calcular puntajes de prioridad
    df['priority_score'] = df.apply(calculate_priority_score, axis=1)
    
    # Calcular pacientes perdidos
    lost_count = 0
    control_compliant = 0
    medication_compliant = 0
    exam_compliant = 0
    
    for _, row in df.iterrows():
        is_lost, _ = is_lost_patient(row)
        if is_lost:
            lost_count += 1
        
        # Verificar cumplimiento
        if days_since_date(row['last_control']) <= 180:
            control_compliant += 1
        
        if days_since_date(row['last_medication']) <= 90:
            medication_compliant += 1
        
        if days_since_date(row['last_exam']) <= 365:
            exam_compliant += 1
    
    total_patients = len(df)
    high_risk_count = len(df[df['priority_score'] > 70])
    
    # Distribución de factores de riesgo
    diabetes_count = len(df[df['diabetes'] == 'Yes'])
    hypertension_count = len(df[df['hypertension'] == 'Yes'])
    smoker_count = len(df[df['smoker'] == 'Yes'])
    
    # Eventos previos
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
