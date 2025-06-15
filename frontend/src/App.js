import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [code, setCode] = useState('');
  const [documentation, setDocumentation] = useState('');

  const generateDocumentation = async () => {
    try {
      const response = await axios.post('http://localhost:5000/generate-doc', { code });
      setDocumentation(response.data.doc || response.data.suggestions || 'No documentation returned.');
    } catch (error) {
      setDocumentation('Something went wrong. Please try again.');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial', maxWidth: '800px', margin: 'auto' }}>
      <h2>AI Code Documentation Generator</h2>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={10}
        cols={80}
        placeholder="Type your Python code here..."
        style={{ width: '100%', fontFamily: 'monospace', fontSize: '16px' }}
      />
      <br /><br />
      <p>As we are using a agents in the backend, it takes time to generate correct output. Please wait patiently before retrying.</p>
      <button onClick={generateDocumentation}>Generate Documentation</button>
      <h3>Output:</h3>
      <pre style={{ backgroundColor: '#f4f4f4', padding: '10px', textWrap: 'wrap' }}>{documentation}</pre>
    </div>
  );
}

export default App;
