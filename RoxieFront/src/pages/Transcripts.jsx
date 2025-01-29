import React, { useState, useEffect } from "react";
import { FaArrowRight } from "react-icons/fa";
import Navbar from "../components/Navbar";

const Transcripts = () => {
  const [transcripts, setTranscripts] = useState([]);
  const [selectedTranscript, setSelectedTranscript] = useState(null);

  useEffect(() => {
    const fetchTranscripts = async () => {
      try {
        console.log("hit");
        const response = await fetch("http://localhost:3000/api/transcripts");
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        if (Array.isArray(data) && data.length > 0) {
          setTranscripts(data);
          setSelectedTranscript(data[0]); // Select first transcript by default
        }
      } catch (error) {
        console.error("Error fetching transcripts:", error);
      }
    };

    fetchTranscripts();
  }, []);

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
            {transcripts.length > 0 ? (
              transcripts.map((transcript) => (
                <div
                  key={transcript._id}
                  style={styles.transcriptItem}
                  onClick={() => handleTranscriptClick(transcript)}
                >
                  <span>{transcript.user_info.name}</span>
                  <FaArrowRight style={styles.arrowIcon} />
                </div>
              ))
            ) : (
              <p style={styles.loadingText}>No transcripts available.</p>
            )}
          </div>
        </div>

        {selectedTranscript && (
          <div style={styles.rightPane}>
            <h3>{selectedTranscript.name}</h3>
            <p>
              <strong>Description:</strong> {selectedTranscript.user_info.name}
            </p>
            {Array.isArray(selectedTranscript.transcript) ? (
              selectedTranscript.transcript.map((line, index) => (
                <li key={index}>{line}</li>
              ))
            ) : (
              <p>No transcript content available.</p>
            )}
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
  loadingText: {
    color: "white",
    textAlign: "center",
  },
};

export default Transcripts;
