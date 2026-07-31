import { useState, useEffect } from 'react';
import WorkerLookup from './WorkerLookup';
import ContractorDashboard from './ContractorDashboard';

function App() {
  const [view, setView] = useState('log'); // 'log', 'lookup', or 'dashboard'

  const [workers, setWorkers] = useState([]);
  const [sites, setSites] = useState([]);
  const [workerId, setWorkerId] = useState('');
  const [siteId, setSiteId] = useState('');
  const [status, setStatus] = useState('present');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/workers')
      .then(res => res.json())
      .then(data => setWorkers(data));

    fetch('http://127.0.0.1:8000/sites')
      .then(res => res.json())
      .then(data => setSites(data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const today = new Date().toISOString().split('T')[0];

    const response = await fetch('http://127.0.0.1:8000/attendance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        worker_id: parseInt(workerId),
        site_id: parseInt(siteId),
        date: today,
        status: status
      })
    });

    if (response.ok) {
      setMessage('Attendance logged successfully!');
    } else {
      setMessage('Something went wrong. Try again.');
    }
  };

  return (
    <div>
      <div style={{ textAlign: 'center', padding: '15px' }}>
        <button onClick={() => setView('log')} style={{ marginRight: '10px' }}>
          Log Attendance
        </button>
        <button onClick={() => setView('lookup')} style={{ marginRight: '10px' }}>
          Check My Score
        </button>
        <button onClick={() => setView('dashboard')}>
          Contractor Dashboard
        </button>
      </div>

      {view === 'log' && (
        <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
          <h1>Log Attendance</h1>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <label>Worker</label><br />
              <select value={workerId} onChange={(e) => setWorkerId(e.target.value)} required>
                <option value="">Select worker</option>
                {workers.map(w => (
                  <option key={w.id} value={w.id}>{w.name}</option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label>Site</label><br />
              <select value={siteId} onChange={(e) => setSiteId(e.target.value)} required>
                <option value="">Select site</option>
                {sites.map(s => (
                  <option key={s.id} value={s.id}>{s.site_name}</option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label>Status</label><br />
              <select value={status} onChange={(e) => setStatus(e.target.value)}>
                <option value="present">Present</option>
                <option value="absent">Absent</option>
              </select>
            </div>

            <button type="submit">Submit</button>
          </form>

          {message && <p>{message}</p>}
        </div>
      )}

      {view === 'lookup' && <WorkerLookup />}
      {view === 'dashboard' && <ContractorDashboard />}
    </div>
  );
}

export default App;