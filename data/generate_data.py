import csv
import random
from datetime import datetime, timedelta

def generate_dummy_data(num_patients=100):
    """Generar datos de prueba de pacientes cardiovasculares"""
    
    first_names = ["Juan", "María", "Carlos", "Ana", "José", "Carmen", "Antonio", "Isabel", 
                   "Francisco", "Dolores", "Manuel", "Pilar", "David", "Mercedes", "Javier"]
    last_names = ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", 
                  "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández"]
    
    today = datetime.now()
    
    patients = []
    
    for i in range(1, num_patients + 1):
        # Información básica
        patient_id = f"PAT{i:04d}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(45, 85)
        gender = random.choice(["M", "F"])
        
        # Parámetros clínicos
        systolic_bp = random.randint(100, 180)
        diastolic_bp = random.randint(60, 110)
        cholesterol = random.randint(150, 300)
        ldl = random.randint(70, 200)
        hdl = random.randint(30, 80)
        glucose = random.randint(70, 250)
        bmi = round(random.uniform(20, 38), 1)
        
        # Factores de riesgo
        smoker = random.choice(["Yes", "No"])
        diabetes = random.choice(["Yes", "No"])
        hypertension = random.choice(["Yes", "No"])
        
        # Fechas de último control/medicamento/examen
        # Algunos pacientes están "perdidos" con fechas antiguas
        if random.random() < 0.3:  # 30% pacientes perdidos
            days_since_control = random.randint(181, 400)
            days_since_medication = random.randint(91, 300)
            days_since_exam = random.randint(366, 500)
        else:
            days_since_control = random.randint(0, 180)
            days_since_medication = random.randint(0, 90)
            days_since_exam = random.randint(0, 365)
        
        last_control = (today - timedelta(days=days_since_control)).strftime("%Y-%m-%d")
        last_medication = (today - timedelta(days=days_since_medication)).strftime("%Y-%m-%d")
        last_exam = (today - timedelta(days=days_since_exam)).strftime("%Y-%m-%d")
        
        # Adherencia a medicamentos
        medication_compliance = random.choice(["High", "Medium", "Low"])
        
        # Eventos previos
        previous_mi = random.choice(["Yes", "No"])
        previous_stroke = random.choice(["Yes", "No"])
        
        patients.append({
            "patient_id": patient_id,
            "name": name,
            "age": age,
            "gender": gender,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "cholesterol": cholesterol,
            "ldl": ldl,
            "hdl": hdl,
            "glucose": glucose,
            "bmi": bmi,
            "smoker": smoker,
            "diabetes": diabetes,
            "hypertension": hypertension,
            "last_control": last_control,
            "last_medication": last_medication,
            "last_exam": last_exam,
            "medication_compliance": medication_compliance,
            "previous_mi": previous_mi,
            "previous_stroke": previous_stroke
        })
    
    return patients

def save_to_csv(patients, filename="patients_data.csv"):
    """Guardar datos de pacientes en CSV"""
    if not patients:
        return
    
    fieldnames = patients[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(patients)
    
    print(f"Generados {len(patients)} registros de pacientes en {filename}")

if __name__ == "__main__":
    patients = generate_dummy_data(100)
    save_to_csv(patients, "data/patients_data.csv")
