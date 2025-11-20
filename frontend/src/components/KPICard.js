import React from 'react';
import './KPICard.css';

function KPICard({ title, value, subtitle, icon, color }) {
  return (
    <div className="kpi-card" style={{ borderLeftColor: color }}>
      <div className="kpi-icon" style={{ backgroundColor: color }}>
        {icon}
      </div>
      <div className="kpi-content">
        <h3>{title}</h3>
        <div className="kpi-value">{value}</div>
        {subtitle && <div className="kpi-subtitle">{subtitle}</div>}
      </div>
    </div>
  );
}

export default KPICard;
