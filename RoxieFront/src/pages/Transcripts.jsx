import React, { useState } from "react";
import { FaArrowRight } from "react-icons/fa";
import Navbar from "../components/Navbar";

const Transcripts = () => {
  const transcripts = Array.from({ length: 20 }, (_, index) => ({
    name: `Transcript ${index + 1}`,
    description: `This is the description for Transcript ${
      index + 1
    }. It contains detailed information about the transcript.`,
    content: `This is the detailed content of Transcript ${
      index + 1
    }. It includes all the important points and information related to the transcript.`,
  }));

  const [selectedTranscript, setSelectedTranscript] = useState(transcripts[0]);

  const handleTranscriptClick = (transcript) => {
    setSelectedTranscript(transcript);
  };

  return (
    <div style={styles.wrapper}>
      <Navbar />
      <div style={styles.container}>
        <div className="leftPane" style={styles.leftPane}>
          <h2 style={styles.title}>Transcripts</h2>
          <div style={styles.transcriptsList}>
            {transcripts.map((transcript, index) => (
              <div
                key={index}
                style={styles.transcriptItem}
                onClick={() => handleTranscriptClick(transcript)}
              >
                <span>{transcript.name}</span>
                <FaArrowRight style={styles.arrowIcon} />
              </div>
            ))}
          </div>
        </div>

        {selectedTranscript && (
          <div style={styles.rightPane}>
            <h3>{selectedTranscript.name}</h3>
            <p>
              <strong>Description:</strong> {selectedTranscript.description}
            </p>
            <p>
              <strong>Content:</strong> {selectedTranscript.content}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  wrapper: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    backgroundColor: "transparent",
  },
  container: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    padding: "20px",
    width: "80%",
    maxWidth: "1200px",
    height: "auto",
    marginTop: "100px",
  },
  leftPane: {
    width: "40%",
    maxHeight: "400px",
    overflowY: "auto",
    paddingRight: "20px",
    paddingLeft: "20px",
    paddingTop: "10px",
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    borderRadius: "15px",
    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
  },
  title: {
    color: "white",
    fontSize: "24px",
    marginBottom: "20px",
    textAlign: "center",
  },
  transcriptsList: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  transcriptItem: {
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    padding: "15px",
    width: "100%",
    textAlign: "center",
    borderRadius: "10px",
    cursor: "pointer",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    transition: "transform 0.2s",
    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
  },
  arrowIcon: {
    fontSize: "20px",
    marginLeft: "10px",
  },
  rightPane: {
    width: "50%",
    padding: "20px",
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    borderRadius: "15px",
    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
    marginLeft: "20px",
  },
};

export default Transcripts;
