import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const MOCK_DATA = {
  labels: ['Compute', 'Storage', 'Network', 'Database', 'Cache'],
  datasets: [
    {
      label: 'Monthly Cost (USD)',
      data: [15000, 3000, 1200, 8000, 500],
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
    },
  ],
};

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Simulate API fetch
    setTimeout(() => {
      setData(MOCK_DATA);
    }, 500);
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>FinOps Cost Dashboard</h1>
      <p>Analyze your cloud spend across different service categories.</p>
      
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        {data ? (
          <Bar 
            data={data} 
            options={{
              responsive: true,
              plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Cloud Spend Breakdown' }
              }
            }} 
          />
        ) : (
          <p>Loading cost metrics...</p>
        )}
      </div>
    </div>
  );
}

export default App;
