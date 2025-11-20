# CardioHealth Monitoring System ❤️

Un prototipo funcional para el monitoreo de salud cardiovascular que calcula puntajes de prioridad, identifica pacientes “perdidos” y genera indicadores (KPIs) para equipos de salud.

## Características

- **Cálculo de Prioridad**: Genera un puntaje de riesgo cardiovascular (0–100) basado en parámetros clínicos y factores de riesgo.
- **Detección de Pacientes Perdidos**: Identifica pacientes con brechas en la continuidad del cuidado:
  - Sin control por más de 180 días
  - Sin retiro de medicamentos por más de 90 días
  - Exámenes vencidos (>365 días)
- **Auditoría de KPIs**: Dashboard con:
  - Métricas de cumplimiento
  - Distribución de factores de riesgo
  - Análisis del puntaje de riesgo
- **Backend FastAPI**: API REST con tres endpoints: (`/priority`, `/lost`, `/audit`)
- **Dashboard en React**: Interfaz interactiva con tablas, tarjetas KPI y visualización de datos.

## Arquitectura

```
HackathonSaludIA/
├── backend/
│   ├── main.py              # FastAPI application with endpoints
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── KPICard.js
│   │   │   ├── PriorityTable.js
│   │   │   └── LostPatientsTable.js
│   │   ├── App.js          # Main React app
│   │   └── index.js
│   └── package.json        # Node dependencies
└── data/
    ├── generate_data.py    # Dummy data generator
    └── patients_data.csv   # Sample patient records
```

## Algoritmo de Puntaje de Prioridad

El sistema utiliza un algoritmo basado en reglas que considera:
- **Edad** (0–15 pts) — mayor edad, mayor puntuación
- **Presión arterial** (0–20 pts) — ≥160/100 obtiene puntaje máximo
- **Colesterol/LDL** (0–15 pts) — colesterol ≥240 o LDL ≥160
- **Glucosa** (0–15 pts) — indicadores de diabetes (≥200)
- **IMC** (0–10 pts) — sobrepeso y obesidad
- **Factores de riesgo** (0–25 pts) — HTA, DM2, tabaquismo
- **Eventos previos** (0–15 pts) — IAM o ACV
- **Adherencia a medicamentos** (0–10 pts) — baja adherencia penaliza
Puntaje máximo: 100 puntos

## Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Node.js 14+
- npm o yarn

### Configuración del Backend

1. Ir a la carpeta backend:
```bash
cd backend
```
2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate
```
3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Configuración del Frontend

1. Ir a la carpeta frontend:
```bash
cd frontend
```
2. Instalar dependencias:
```bash
npm install
```
### Generar Datos Dummy

```bash
cd ..
python data\generate_data.py
```
Esto genera 100 registros de pacientes con datos cardiovasculares realistas.

## Ejecutar la Aplicación

### Iniciar Backend

```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload #Ejecutar FastAPI con Uvicorn:

python main.py
```

Backend disponible en: `http://localhost:8000`

Documentación Swagger: `http://localhost:8000/docs`

### Iniciar Frontend
En otra terminal:

```bash
cd frontend
npm start
```

Dashboard en: `http://localhost:3000`

## Endpoints de la API

### GET /priority
Retorna pacientes ordenados por puntaje de riesgo cardiovascular.

**Response:**
```json
{
  "total_patients": 100,
  "patients": [
    {
      "patient_id": "PAT0001",
      "name": "Juan García",
      "age": 75,
      "priority_score": 87,
      ...
    }
  ],
  "score_info": {
    "max_score": 100,
    "description": "Puntajes más altos indican mayor riesgo cardiovascular"
  }
}
```

### GET /lost
Identifica pacientes “perdidos” con detalles de brechas.

**Response:**
```json
{
  "total_lost": 30,
  "patients": [
    {
      "patient_id": "PAT0023",
      "name": "María Rodríguez",
      "days_since_control": 245,
      "days_since_medication": 120,
      "days_since_exam": 400,
      "lost_reasons": [
        "Sin visita de control en 245 días",
        "Sin retiro de medicamentos en 120 días",
        "Exámenes pendientes (400 días)"
      ]
    }
  ],
  "thresholds": {
    "control_visit": "180 días",
    "medication_pickup": "90 días",
    "exam": "365 días"
  }
}
```

### GET /audit
Devuelve KPIs de auditoría cardiovascular.

**Response:**
```json
{
  "total_patients": 100,
  "high_risk_patients": {
    "count": 25,
    "percentage": 25.0
  },
  "lost_patients": {
    "count": 30,
    "percentage": 30.0
  },
  "compliance": {
    "control_visits": { "compliant": 70, "percentage": 70.0 },
    "medication_pickup": { "compliant": 72, "percentage": 72.0 },
    "exams": { "compliant": 68, "percentage": 68.0 }
  },
  "risk_factors": {
    "diabetes": { "count": 35, "percentage": 35.0 },
    "hypertension": { "count": 45, "percentage": 45.0 },
    "smokers": { "count": 28, "percentage": 28.0 }
  },
  "average_risk_score": 52.3,
  "score_distribution": {
    "low_risk": 35,
    "medium_risk": 40,
    "high_risk": 25
  }
}
```

## Características del Dashboard

### Tarjetas KPI
- Total de pacientes, contador de pacientes en total.
- Alto riesgo (>70 su puntaje)
- Pacientes perdidos
- Promedio puntaje de riesgo

### Tabla de Prioridad
- Ordenada por riesgo (altos primeros)
- Colores según nivel (alto/medio/bajo)
- Factores clínicos y adherencia
- - Se muestra los factores de riesgo

### Tabla de Pacientes Perdidos
- Lista los pacientes con brechas específicas
- Destaca métricas vencidas en rojo
- Marca pacientes con múltiples brechas

### KPIs de Auditoría
- Cumplimiento de controles
- Retiro de medicamentos
- Exámenes realizados
- Distribución de factores de riesgo

## Tecnologías Utilizadas

**Backend:**
- FastAPI 0.104.1
- Pandas 2.1.3
- Uvicorn 0.24.0

**Frontend:**
- React 18.2.0
- Axios 1.6.0
- CSS3

**Data:**
- Formato CSV
- Generación de datos con Python

## Mejoras Futuras
- Modelo ML para predicción de riesgo
- Filtros avanzados y búsqueda
- Exportar reportes (PDF/Excel)
- Alertas a profesionales
- Integración con sistemas clínicos (EHR)
- Análisis de tendencias históricas

## Licencia

MIT License – Construido para Hackathon SaludIA

## Contribuidores

Desarrollado con ❤️ para mejorar los resultados en salud cardiovascular.
