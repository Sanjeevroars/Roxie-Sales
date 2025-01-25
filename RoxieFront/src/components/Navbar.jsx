import React, { useEffect } from "react";
import { gsap } from "gsap";
import "./Navbar.css";
import logo from "../assets/logor.png";

const Navbar = () => {
  useEffect(() => {
    gsap.fromTo(
      ".navbar",
      {
        opacity: 0,
        y: -50,
      },
      {
        opacity: 1,
        y: 0,
        duration: 2,
        ease: "power2.out",
      }
    );
  }, []);

  return (
    <nav className="navbar">
      <div className="logo">
        <img src={logo} alt="Logo" className="logo-img" />
      </div>
      <div className="nav-buttons">
        <ul className="nav-links">
          <li>
            <a href="#home">Home</a>
          </li>
          <li>
            <a href="#roxie">Roxie</a>
          </li>
          <li>
            <a href="#dashboard">Transcript</a>
          </li>
          <li>
            <a href="#transcript" id="transcript-link">
              Dashboard
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
