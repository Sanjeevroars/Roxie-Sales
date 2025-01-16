import React, { useEffect, useState } from 'react';
import TranscriptList from './TranscriptList';
import Transcript from './Transcript';
import './App.css';

function App() {
  const [transcripts, setTranscripts] = useState([]);
  const [selectedTranscript, setSelectedTranscript] = useState(null);

  useEffect(() => {
    fetch('/api/list_transcripts')
      .then(response => response.json())
      .then(data => setTranscripts(data.transcripts));
  }, []);

  const loadTranscript = (filename) => {
    fetch(`/api/load_transcript/${filename}`)
      .then(response => response.json())
      .then(data => setSelectedTranscript(data.transcript));
  };

  return (
    <div className="App">
      <h1>Saved Conversation Transcripts</h1>
      <TranscriptList transcripts={transcripts} onTranscriptClick={loadTranscript} />
      {selectedTranscript && <Transcript transcript={selectedTranscript} />}
    </div>
  );
}

export default App;
