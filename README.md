# CardioHealth Monitoring System 🫀

A functional prototype for cardiovascular health monitoring that tracks patient priority scores, identifies lost patients, and generates audit KPIs for healthcare providers.

## Features

- **Priority Scoring**: Calculates cardiovascular risk scores (0-100) based on clinical parameters and risk factors
- **Lost Patient Detection**: Identifies patients with gaps in care:
  - No control visit in >180 days
  - No medication pickup in >90 days  
  - Missing exams (>365 days)
- **Audit KPIs**: Comprehensive dashboard with compliance metrics, risk factor distribution, and score analytics
- **FastAPI Backend**: RESTful API with three endpoints (`/priority`, `/lost`, `/audit`)
- **React Dashboard**: Interactive UI with tables, KPI cards, and real-time data visualization

## Architecture

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

## Priority Scoring Algorithm

The system uses a rule-based scoring algorithm that considers:

- **Age** (0-15 points): Higher scores for older patients (75+, 65-74, 55-64)
- **Blood Pressure** (0-20 points): Systolic ≥160 or Diastolic ≥100 gets maximum points
- **Cholesterol/LDL** (0-15 points): High cholesterol (≥240) or LDL (≥160)
- **Glucose** (0-15 points): Diabetes indicators (≥200)
- **BMI** (0-10 points): Obesity levels (≥35, ≥30, ≥25)
- **Risk Factors** (0-25 points): Diabetes, Hypertension, Smoking
- **Previous Events** (0-15 points): Prior MI or Stroke
- **Medication Compliance** (0-10 points): Low/Medium compliance penalty

Maximum score: **100 points**

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Generate Dummy Data

```bash
cd ..
python data\generate_data.py
```

This generates 100 patient records with realistic cardiovascular data.

## Running the Application

### Start Backend Server

```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload #Run FastAPI with Uvicorn:

python main.py
```

Backend will run at: `http://localhost:8000`

API Documentation (Swagger): `http://localhost:8000/docs`

### Start Frontend Dashboard

In a new terminal:

```bash
cd frontend
npm start
```

Frontend will run at: `http://localhost:3000`

## API Endpoints

### GET /priority
Returns patients sorted by cardiovascular risk score (highest priority first).

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
    "description": "Higher scores indicate higher cardiovascular risk"
  }
}
```

### GET /lost
Returns patients lost to follow-up with gap details.

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
        "No control visit in 245 days",
        "No medication pickup in 120 days",
        "Missing exams (400 days)"
      ]
    }
  ],
  "thresholds": {
    "control_visit": "180 days",
    "medication_pickup": "90 days",
    "exam": "365 days"
  }
}
```

### GET /audit
Returns comprehensive audit KPIs.

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

## Dashboard Features

### KPI Cards
- **Total Patients**: Overall patient count
- **High Risk**: Patients with score >70
- **Lost Patients**: Patients with care gaps
- **Average Risk Score**: Mean priority score

### Priority Patients Table
- Sorted by risk score (highest first)
- Shows clinical parameters, risk factors, compliance
- Color-coded risk levels (High/Medium/Low)

### Lost Patients Table
- Lists patients with care gaps
- Highlights overdue metrics in red
- Shows specific reasons for being "lost"
- Critical patients (3+ gaps) highlighted

### Audit KPIs
- Compliance metrics (control visits, medication, exams)
- Risk factor distribution
- Previous cardiovascular events
- Risk score distribution

## Technology Stack

**Backend:**
- FastAPI 0.104.1
- Pandas 2.1.3
- Uvicorn 0.24.0

**Frontend:**
- React 18.2.0
- Axios 1.6.0
- CSS3 (Custom styling)

**Data:**
- CSV format
- Python data generation

## Future Enhancements

- Machine Learning risk prediction models
- Patient search and filtering
- Export reports to PDF/Excel
- Email notifications for high-risk patients
- Integration with EHR systems
- Historical trend analysis
- Mobile-responsive design improvements

## License

MIT License - Built for Hackathon SaludIA

## Contributors

Built with ❤️ for improving cardiovascular healthcare outcomes
