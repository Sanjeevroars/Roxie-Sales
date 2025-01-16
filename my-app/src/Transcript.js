import React from 'react';

function Transcript({ transcript }) {
  return (
    <div id="transcript">
      {transcript.transcript.map((line, index) => (
        <p key={index} className="line">{line}</p>
      ))}
    </div>
  );
}

export default Transcript;
