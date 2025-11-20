import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import KPICard from './components/KPICard';
import PriorityTable from './components/PriorityTable';
import LostPatientsTable from './components/LostPatientsTable';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('priority');
  const [priorityData, setPriorityData] = useState(null);
  const [lostData, setLostData] = useState(null);
  const [auditData, setAuditData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [priorityRes, lostRes, auditRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/priority`),
        axios.get(`${API_BASE_URL}/lost`),
        axios.get(`${API_BASE_URL}/audit`)
      ]);
      
      setPriorityData(priorityRes.data);
      setLostData(lostRes.data);
      setAuditData(auditRes.data);
    } catch (err) {
      setError('Error al cargar los datos. Asegúrate de que el servidor backend esté ejecutándose en el puerto 8000.');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <div className="spinner"></div>
          <p>Cargando datos de pacientes...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>⚠️ Error</h2>
          <p>{error}</p>
          <button onClick={fetchAllData} className="retry-btn">Reintentar</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="header-title">
            <h1>
              <img
                src={`${process.env.PUBLIC_URL}/heart2.png`}
                alt="heart icon"
                className="header-icon-inline"
              />
              CardioHealth Sistema de Monitoreo
            </h1>
            <p className="subtitle">Panel de Gestión de Pacientes Cardiovasculares</p>
          </div>
        </div>
      </header>

      {auditData && (
        <div className="kpi-section">
          <KPICard
            title="Total de Pacientes"
            value={auditData.total_patients}
            icon="👥"
            color="#4a90e2"
          />
          <KPICard
            title="Alto Riesgo"
            value={auditData.high_risk_patients.count}
            subtitle={`${auditData.high_risk_patients.percentage}%`}
            icon="⚠️"
            color="#e74c3c"
          />
          <KPICard
            title="Pacientes Perdidos"
            value={auditData.lost_patients.count}
            subtitle={`${auditData.lost_patients.percentage}%`}
            icon="🔍"
            color="#f39c12"
          />
          <KPICard
            title="Puntaje de Riesgo Promedio"
            value={auditData.average_risk_score}
            subtitle="de 100"
            icon="📊"
            color="#9b59b6"
          />
        </div>
      )}

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'priority' ? 'active' : ''}`}
          onClick={() => setActiveTab('priority')}
        >
          Pacientes Prioritarios
        </button>
        <button
          className={`tab ${activeTab === 'lost' ? 'active' : ''}`}
          onClick={() => setActiveTab('lost')}
        >
          Pacientes Perdidos ({lostData?.total_lost || 0})
        </button>
        <button
          className={`tab ${activeTab === 'audit' ? 'active' : ''}`}
          onClick={() => setActiveTab('audit')}
        >
          KPIs de Auditoría
        </button>
      </div>

      <div className="content">
        {activeTab === 'priority' && priorityData && (
          <PriorityTable data={priorityData} />
        )}

        {activeTab === 'lost' && lostData && (
          <LostPatientsTable data={lostData} />
        )}

        {activeTab === 'audit' && auditData && (
          <div className="audit-section">
            <div className="audit-grid">
              <div className="audit-card">
                <h3>Métricas de Cumplimiento</h3>
                <div className="metric-row">
                  <span>Visitas de Control (≤180 días)</span>
                  <span className="metric-value">
                    {auditData.compliance.control_visits.percentage}%
                  </span>
                </div>
                <div className="metric-row">
                  <span>Retiro de Medicamentos (≤90 días)</span>
                  <span className="metric-value">
                    {auditData.compliance.medication_pickup.percentage}%
                  </span>
                </div>
                <div className="metric-row">
                  <span>Exámenes (≤365 días)</span>
                  <span className="metric-value">
                    {auditData.compliance.exams.percentage}%
                  </span>
                </div>
              </div>

              <div className="audit-card">
                <h3>Distribución de Factores de Riesgo</h3>
                <div className="metric-row">
                  <span>Diabetes</span>
                  <span className="metric-value">
                    {auditData.risk_factors.diabetes.count} ({auditData.risk_factors.diabetes.percentage}%)
                  </span>
                </div>
                <div className="metric-row">
                  <span>Hipertensión</span>
                  <span className="metric-value">
                    {auditData.risk_factors.hypertension.count} ({auditData.risk_factors.hypertension.percentage}%)
                  </span>
                </div>
                <div className="metric-row">
                  <span>Fumadores</span>
                  <span className="metric-value">
                    {auditData.risk_factors.smokers.count} ({auditData.risk_factors.smokers.percentage}%)
                  </span>
                </div>
              </div>

              <div className="audit-card">
                <h3>Eventos Previos</h3>
                <div className="metric-row">
                  <span>Infarto de Miocardio</span>
                  <span className="metric-value">
                    {auditData.previous_events.myocardial_infarction.count} ({auditData.previous_events.myocardial_infarction.percentage}%)
                  </span>
                </div>
                <div className="metric-row">
                  <span>ACV</span>
                  <span className="metric-value">
                    {auditData.previous_events.stroke.count} ({auditData.previous_events.stroke.percentage}%)
                  </span>
                </div>
              </div>

              <div className="audit-card">
                <h3>Distribución de Puntaje de Riesgo</h3>
                <div className="metric-row">
                  <span>Riesgo Bajo (&lt;40)</span>
                  <span className="metric-value">
                    {auditData.score_distribution.low_risk}
                  </span>
                </div>
                <div className="metric-row">
                  <span>Riesgo Medio (40-70)</span>
                  <span className="metric-value">
                    {auditData.score_distribution.medium_risk}
                  </span>
                </div>
                <div className="metric-row">
                  <span>Riesgo Alto (&gt;70)</span>
                  <span className="metric-value">
                    {auditData.score_distribution.high_risk}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
