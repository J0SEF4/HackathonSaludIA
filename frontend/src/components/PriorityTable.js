import React from 'react';
import './PriorityTable.css';

function PriorityTable({ data }) {
  const getRiskLevel = (score) => {
    if (score > 70) return { text: 'High', class: 'high' };
    if (score >= 40) return { text: 'Medium', class: 'medium' };
    return { text: 'Low', class: 'low' };
  };

  return (
    <div className="table-container">
      <div className="table-header">
        <h2>Priority Patients (Sorted by Risk Score)</h2>
        <p className="table-description">
          Total: {data.total_patients} patients | Score range: 0-100
        </p>
      </div>
      
      <div className="table-wrapper">
        <table className="priority-table">
          <thead>
            <tr>
              <th>Patient ID</th>
              <th>Name</th>
              <th>Age</th>
              <th>Gender</th>
              <th>BP (S/D)</th>
              <th>Cholesterol</th>
              <th>Glucose</th>
              <th>Risk Factors</th>
              <th>Compliance</th>
              <th>Priority Score</th>
              <th>Risk Level</th>
            </tr>
          </thead>
          <tbody>
            {data.patients.map((patient) => {
              const riskLevel = getRiskLevel(patient.priority_score);
              const riskFactors = [];
              if (patient.diabetes === 'Yes') riskFactors.push('DM');
              if (patient.hypertension === 'Yes') riskFactors.push('HTN');
              if (patient.smoker === 'Yes') riskFactors.push('Smoker');
              
              return (
                <tr key={patient.patient_id}>
                  <td className="patient-id">{patient.patient_id}</td>
                  <td className="patient-name">{patient.name}</td>
                  <td>{patient.age}</td>
                  <td>{patient.gender}</td>
                  <td>{patient.systolic_bp}/{patient.diastolic_bp}</td>
                  <td>{patient.cholesterol}</td>
                  <td>{patient.glucose}</td>
                  <td>
                    {riskFactors.length > 0 ? (
                      <div className="risk-factors">
                        {riskFactors.map((rf, idx) => (
                          <span key={idx} className="risk-badge">{rf}</span>
                        ))}
                      </div>
                    ) : (
                      <span className="none">None</span>
                    )}
                  </td>
                  <td>
                    <span className={`compliance ${patient.medication_compliance.toLowerCase()}`}>
                      {patient.medication_compliance}
                    </span>
                  </td>
                  <td>
                    <span className="score">{patient.priority_score}</span>
                  </td>
                  <td>
                    <span className={`risk-level ${riskLevel.class}`}>
                      {riskLevel.text}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PriorityTable;
