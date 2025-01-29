import React from "react";
import { Link } from "react-router-dom";

const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img src="/product-img.png" alt="Hero Image" />
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <p>Rating: {product.rating}</p>
      <Link to={`/products/${product._id}`}>View Details</Link>
      <br/>
      <br/>
      <button className="px-5 py-2 bg-black text-white font-semibold shadow-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-300">
  Add to Cart
</button>
    </div>
  );
};

export default ProductCard;
