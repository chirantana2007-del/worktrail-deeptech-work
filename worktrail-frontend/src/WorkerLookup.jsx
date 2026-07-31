import { useState } from 'react';

function WorkerLookup() {
  const [phone, setPhone] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleLookup = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    const response = await fetch(`http://127.0.0.1:8000/reliability/${phone}`);
    const data = await response.json();

    if (data.error) {
      setError(data.error);
    } else {
      setResult(data);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h1 style={{ lineHeight: '1.3', marginBottom: '20px' }}>Check Your Reliability Score</h1>
      <form onSubmit={handleLookup}>
        <label>Phone Number</label><br />
        <input
          type="text"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="Enter your phone number"
          required
        />
        <br /><br />
        <button type="submit">Check Score</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '15px' }}>
          <h2>{result.worker_name}</h2>
          <p><strong>Reliability Score:</strong> {result.reliability_score} / 100</p>
          <p>Attendance rate: {(result.attendance_rate * 100).toFixed(0)}%</p>
          <p>Tenure: {result.tenure_days} days</p>
          <p>Sites worked: {result.num_sites}</p>
          <p>Total days logged: {result.total_days_logged}</p>
        </div>
      )}
    </div>
  );
}

export default WorkerLookup;