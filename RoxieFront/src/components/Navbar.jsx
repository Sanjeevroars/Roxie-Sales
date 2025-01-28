import React, { useEffect } from "react";
import { gsap } from "gsap";
import { Link } from "react-router-dom";
import "./Navbar.css";
// import logo from "../assets/logor.png";

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
        <img src="/logor.png" alt="Logo" className="logo-img" />
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
            <Link to="/transcripts">Transcript</Link>
          </li>
          <li>
            <a href="#dashboard" id="dashboard-link">
              Dashboard
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
