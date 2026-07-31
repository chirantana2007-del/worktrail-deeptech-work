import { useState, useEffect } from 'react';

function ContractorDashboard() {
  const [allWorkers, setAllWorkers] = useState([]);
  const [minScore, setMinScore] = useState(0);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/reliability/all')
      .then(res => res.json())
      .then(data => setAllWorkers(data));
  }, []);

  const filteredWorkers = allWorkers.filter(w => w.reliability_score >= minScore);

  return (
    <div style={{ padding: '20px', maxWidth: '700px', margin: '0 auto' }}>
      <h1 style={{ lineHeight: '1.3', marginBottom: '20px' }}>Worker Reliability Directory</h1>

      <div style={{ marginBottom: '20px' }}>
        <label>Minimum reliability score: {minScore}</label><br />
        <input
          type="range"
          min="0"
          max="100"
          value={minScore}
          onChange={(e) => setMinScore(Number(e.target.value))}
          style={{ width: '300px' }}
        />
      </div>

      <p>{filteredWorkers.length} worker(s) match this filter</p>

      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #555', textAlign: 'left' }}>
            <th style={{ padding: '8px' }}>Name</th>
            <th style={{ padding: '8px' }}>Score</th>
            <th style={{ padding: '8px' }}>Attendance</th>
            <th style={{ padding: '8px' }}>Tenure</th>
            <th style={{ padding: '8px' }}>Sites</th>
          </tr>
        </thead>
        <tbody>
          {filteredWorkers.map(w => (
            <tr key={w.worker_id} style={{ borderBottom: '1px solid #333' }}>
              <td style={{ padding: '8px' }}>{w.worker_name}</td>
              <td style={{ padding: '8px' }}>{w.reliability_score}</td>
              <td style={{ padding: '8px' }}>{(w.attendance_rate * 100).toFixed(0)}%</td>
              <td style={{ padding: '8px' }}>{w.tenure_days} days</td>
              <td style={{ padding: '8px' }}>{w.num_sites}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ContractorDashboard;