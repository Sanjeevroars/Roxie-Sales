import React from "react";
import { Link } from "react-router-dom";
import { FaSearch, FaUser, FaShoppingCart, FaGlobe, FaTags, FaServer, FaDesktop, FaTools, FaInfoCircle } from "react-icons/fa";
import FooterPart from "./FooterPart";

const Header = () => {
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
          <Dropdown
            label="Sign In"
            icon={<FaUser />}
            options={["Profile", "Orders", "Logout"]}
          />
          <Link to="/contact" className="hover:underline flex items-center space-x-2">
            <FaInfoCircle className="w-4 h-4" />
            <span>Contact Us</span>
          </Link>
          <Dropdown
            label="IN/EN"
            icon={<FaGlobe />}
            options={["English", "Hindi"]}
          />
          <Dropdown
            label="Cart"
            icon={<FaShoppingCart />}
            options={["View Cart", "Checkout"]}
          />
        </div>
      </div>

      {/* Second Row */}
      <div className="flex justify-start items-center space-x-6 px-4 py-2 border-t mx-5 mb-10">
        
        <Link to="/products" className="hover:underline flex items-center space-x-2">
        <Dropdown
          label="Artificial Intelligence"
          icon={<FaServer />}
          options={["View All Apex", "Compute & HCI", "Storage", "Cyber & Data Protection", "Custom Solutions"]}
        />
        </Link>
        
        <Link to="/products" className="hover:underline flex items-center space-x-2">
        <Dropdown
          label="IT Infrastructure"
          icon={<FaTools />}
          options={["View All Solutions", "Cloud Solutions", "DevOps Tools", "Edge Solutions"]}
        />
        </Link>
        
        <Link to="/products" className="hover:underline flex items-center space-x-2">
        <Dropdown
          label="Computer and Accessories"
          icon={<FaDesktop />}
          options={["Laptops", "Desktops", "Gaming", "Workstations", "Servers", "Monitors"]}
        />
        </Link>
        
        <Link to="/products" className="hover:underline flex items-center space-x-2">
        <Dropdown
          label="Services"
          icon={<FaTools />}
          options={["Consultation", "Deployment", "Support", "Education"]}
        />
        </Link>
        
        <Link to="/products" className="hover:underline flex items-center space-x-2">
        <Dropdown
          label="Support"
          icon={<FaInfoCircle />}
          options={["Support Home", "Warranty", "Drivers", "Documentation"]}
        />
        </Link>
        
        <Link to="/products" className="hover:underline flex items-center space-x-2">
        <Dropdown
          label="Deals"
          icon={<FaTags />}
          options={["Laptop Deals", "Gaming PC Deals", "Workstation Deals"]}
        />
        </Link>
        <Link to="/store" className="hover:underline">
          Find A Store
        </Link>
        
      </div>
    </header>
  );
};

const Dropdown = ({ label, icon, options }) => {
  return (
    <div className="relative group">
      <button className="flex items-center space-x-2 text-gray-700 hover:text-blue-500 focus:outline-none">
        {icon && <span className="w-4 h-4">{icon}</span>}
        <span>{label}</span>
      </button>
      <div className="absolute left-0 mt-2 w-48 bg-white shadow-lg rounded-md opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity duration-300 z-10">
        {options.map((option, index) => (
          <Link
            to="#"
            key={index}
            className="block px-4 py-2 text-sm text-gray-600 hover:bg-blue-100"
          >
            {option}
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Header;
