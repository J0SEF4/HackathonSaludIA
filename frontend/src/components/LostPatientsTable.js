import React from 'react';
import './LostPatientsTable.css';

function LostPatientsTable({ data }) {
  return (
    <div className="table-container">
      <div className="table-header">
        <h2>Lost Patients</h2>
        <p className="table-description">
          Total: {data.total_lost} patients lost to follow-up | Thresholds: Control &gt;{data.thresholds.control_visit}, 
          Medication &gt;{data.thresholds.medication_pickup}, Exams &gt;{data.thresholds.exam}
        </p>
      </div>
      
      <div className="table-wrapper">
        <table className="lost-table">
          <thead>
            <tr>
              <th>Patient ID</th>
              <th>Name</th>
              <th>Age</th>
              <th>Last Control</th>
              <th>Days Since Control</th>
              <th>Last Medication</th>
              <th>Days Since Med</th>
              <th>Last Exam</th>
              <th>Days Since Exam</th>
              <th>Risk Factors</th>
              <th>Lost Reasons</th>
            </tr>
          </thead>
          <tbody>
            {data.patients.map((patient) => {
              const riskFactors = [];
              if (patient.risk_factors.diabetes === 'Yes') riskFactors.push('DM');
              if (patient.risk_factors.hypertension === 'Yes') riskFactors.push('HTN');
              if (patient.risk_factors.smoker === 'Yes') riskFactors.push('Smoker');
              
              return (
                <tr key={patient.patient_id} className={patient.lost_reasons.length >= 3 ? 'critical' : ''}>
                  <td className="patient-id">{patient.patient_id}</td>
                  <td className="patient-name">{patient.name}</td>
                  <td>{patient.age}</td>
                  <td>{patient.last_control}</td>
                  <td>
                    <span className={patient.days_since_control > 180 ? 'warning' : ''}>
                      {patient.days_since_control}
                    </span>
                  </td>
                  <td>{patient.last_medication}</td>
                  <td>
                    <span className={patient.days_since_medication > 90 ? 'warning' : ''}>
                      {patient.days_since_medication}
                    </span>
                  </td>
                  <td>{patient.last_exam}</td>
                  <td>
                    <span className={patient.days_since_exam > 365 ? 'warning' : ''}>
                      {patient.days_since_exam}
                    </span>
                  </td>
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
                    <div className="lost-reasons">
                      {patient.lost_reasons.map((reason, idx) => (
                        <div key={idx} className="reason-badge">
                          {reason}
                        </div>
                      ))}
                    </div>
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

export default LostPatientsTable;
