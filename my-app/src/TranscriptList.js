import React from 'react';

function TranscriptList({ transcripts, onTranscriptClick }) {
  return (
    <div id="transcriptList">
      {transcripts.map((filename, index) => (
        <p key={index} className="transcript-entry" onClick={() => onTranscriptClick(filename)}>
          {filename}
        </p>
      ))}
    </div>
  );
}

export default TranscriptList;
