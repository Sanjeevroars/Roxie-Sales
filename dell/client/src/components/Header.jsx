import React from "react";
import { Link } from "react-router-dom";
import {
  FaSearch,
  FaUser,
  FaShoppingCart,
  FaGlobe,
  FaTags,
  FaServer,
  FaDesktop,
  FaTools,
  FaInfoCircle,
} from "react-icons/fa";

const Header = () => {
  const handleRedirect = (url) => {
    window.location.href = url;
  };

  return (
    <header className="bg-white shadow-md">
      {/* First Row */}
      <div className="flex justify-between items-center p-4 mx-10">
        {/* Logo */}
        <div className="flex-shrink-0">
          <Link to="/" className="text-2xl font-bold text-blue-500">
            <img src="/logo.png" alt="Logo" width="200px" />
          </Link>
        </div>

        {/* Search Bar */}
        <div className="relative w-2/5">
          <input
            type="text"
            placeholder="Search Dell"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <span className="absolute inset-y-0 right-3 flex items-center text-gray-500">
            <FaSearch className="text-gray-500 h-5 w-5" />
          </span>
        </div>

        {/* Right-Side Links */}
        <div className="flex items-center space-x-4">
          <button
            onClick={() => handleRedirect("http://localhost:3000")} // Redirect to the desired URL
            className="flex items-center space-x-2 text-gray-700 hover:text-blue-500"
          >
            <FaGlobe />
            <span>Dashboard</span>
          </button>
        </div>
      </div>

      {/* Second Row */}
      <div className="flex justify-start items-center space-x-6 px-4 py-2 border-t mx-5 mb-10">
        <Link
          to="/products"
          className="hover:underline flex items-center space-x-2"
        >
          <button
            onClick={() => handleRedirect("http://localhost:3001")} // Redirect to the desired URL
            className="flex items-center space-x-2 text-gray-700 hover:text-blue-500"
          >
            <FaServer />
            <span>Artificial Intelligence</span>
          </button>
        </Link>

        <Link
          to="/products"
          className="hover:underline flex items-center space-x-2"
        >
          <button
            onClick={() => handleRedirect("http://localhost:3002")} // Redirect to the desired URL
            className="flex items-center space-x-2 text-gray-700 hover:text-blue-500"
          >
            <FaTools />
            <span>IT Infrastructure</span>
          </button>
        </Link>

        <Link
          to="/products"
          className="hover:underline flex items-center space-x-2"
        >
          <button
            onClick={() => handleRedirect("http://localhost:3003")} // Redirect to the desired URL
            className="flex items-center space-x-2 text-gray-700 hover:text-blue-500"
          >
            <FaDesktop />
            <span>Computer and Accessories</span>
          </button>
        </Link>

        <Link
          to="/products"
          className="hover:underline flex items-center space-x-2"
        >
          <button
            onClick={() => handleRedirect("http://localhost:3004")} // Redirect to the desired URL
            className="flex items-center space-x-2 text-gray-700 hover:text-blue-500"
          >
            <FaTools />
            <span>Services</span>
          </button>
        </Link>

        <Link
          to="/products"
          className="hover:underline flex items-center space-x-2"
        >
          <button
            onClick={() => handleRedirect("http://localhost:3005")} // Redirect to the desired URL
            className="flex items-center space-x-2 text-gray-700 hover:text-blue-500"
          >
            <FaInfoCircle />
            <span>Support</span>
          </button>
        </Link>

        <Link
          to="/products"
          className="hover:underline flex items-center space-x-2"
        >
          <button
            onClick={() => handleRedirect("http://localhost:3006")} // Redirect to the desired URL
            className="flex items-center space-x-2 text-gray-700 hover:text-blue-500"
          >
            <FaTags />
            <span>Deals</span>
          </button>
        </Link>
        <Link to="/store" className="hover:underline">
          Find A Store
        </Link>
      </div>
    </header>
  );
};

export default Header;
