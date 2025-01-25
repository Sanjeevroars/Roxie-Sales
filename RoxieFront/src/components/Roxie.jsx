import React from "react";

const Roxie = () => {
  return (
    <div id="roxie" style={styles.roxieContent}>
      {/* <h1 style={{ color: "white" }}>Welcome to Roxie</h1> */}
      <p style={{ color: "white" }}>
        This is the content for the Roxie section.
      </p>
    </div>
  );
};

const styles = {
  roxieContent: {
    padding: "50px",
    color: "white",
    height: "100%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    opacity: 0,
  },
};

export default Roxie;
