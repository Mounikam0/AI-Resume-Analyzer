import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState("");
  const [result, setResult] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || !role) return alert("Choose role and PDF");
    const fd = new FormData();
    fd.append("file", file);
    fd.append("role", role);
    const res = await fetch("http://localhost:8000/api/v1/analyze/upload", {
      method: "POST",
      body: fd
    });
    const data = await res.json();
    setResult(data.analysis);
  };

  return (
    <div className="app">
      <h1>AI Resume Analyzer</h1>
      <form onSubmit={handleUpload}>
        <input type="file" accept="application/pdf" onChange={e => setFile(e.target.files[0])}/>
        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="">Select role</option>
          <option value="Data Scientist">Data Scientist</option>
          <option value="Frontend Engineer">Frontend Engineer</option>
        </select>
        <button type="submit">Analyze</button>
      </form>

      {result && (
        <div>
          <h2>Score: {result.score}%</h2>
          <div>
            <h3>Found</h3>
            <ul>{result.found_skills.map(s => <li key={s}>{s}</li>)}</ul>
          </div>
          <div>
            <h3>Missing</h3>
            <ul>{result.missing_skills.map(s => <li key={s}>{s}</li>)}</ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
