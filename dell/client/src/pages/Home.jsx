import React, { useEffect, useState } from "react";
import ProductCard from "../components/ProductCard";
import axios from "../api/api";
import Slider from "../components/Slider";
import TopSections from "../components/TopSections";
import { FaPhone } from "react-icons/fa"; // Importing the chat icon

const Home = () => {
  const [latestArrivals, setLatestArrivals] = useState([]);
  const [mostRated, setMostRated] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const { data } = await axios.get("/products");
        setLatestArrivals(data.slice(0, 4)); // Latest 4 products
        setMostRated(
          [...data].sort((a, b) => b.rating - a.rating).slice(0, 4) // Top 4 rated products
        );
      } catch (error) {
        console.error("Error fetching products", error);
      }
    };

    fetchProducts();
  }, []);

  const handleChatButtonClick = async () => {
    try {
      await axios.get("http://localhost:3001/run-exe"); // Make a GET request to trigger the exe
      // alert("The EXE was successfully executed!");
    } catch (error) {
      console.error("Error running the EXE:", error);
      alert("There was an error!");
    }
  };

  return (
    <div className="relative">
      {/* Main content */}
      <div className="slider">
        <Slider />
      </div>
      <TopSections />
      <div className="product-grid">
        {latestArrivals.map((product) => (
          <ProductCard key={product._id} product={product} />
        ))}
      </div>
      <div className="product-grid">
        {mostRated.map((product) => (
          <ProductCard key={product._id} product={product} />
        ))}
      </div>

      {/* Floating Chat Button */}
      <button
        className="fixed bottom-8 right-12 p-4 bg-blue-500 text-white rounded-full shadow-lg z-50 flex items-center justify-center"
        onClick={handleChatButtonClick}
      >
        Call now&nbsp;&nbsp;&nbsp;
        <FaPhone size={16} className="rotate-90" />
      </button>
    </div>
  );
};

export default Home;
