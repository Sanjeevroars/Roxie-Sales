import React, { useEffect, useState } from "react";
import axios from "../api/api";
import ProductCard from "../components/ProductCard";

const Products = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const { data } = await axios.get("/products");
        setProducts(data);
      } catch (error) {
        console.error("Error fetching products", error);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className="flex p-8">
      {/* Left Side: Filters */}
      <div className="w-1/4 bg-gray-100 p-6 rounded-lg">
        <h3 className="text-xl font-semibold mb-4">Filters</h3>

        {/* Category Filter */}
        <div className="mb-4">
          <button className="w-full text-left p-2 border-b">Category</button>
          <div className="p-6">
            <label className="block">
              <input type="checkbox" className="mr-2" />
              Electronics
            </label>
            <label className="block">
              <input type="checkbox" className="mr-2" />
              Furniture
            </label>
          </div>
        </div>

        {/* Price Range Filter */}
        <div className="mb-4">
          <button className="w-full text-left p-2 border-b">Price Range</button>
          <div className="p-6">
            <label className="block">
              <input type="checkbox" className="mr-2" />
              $0 - $100
            </label>
            <label className="block">
              <input type="checkbox" className="mr-2" />
              $100 - $500
            </label>
            <label className="block">
              <input type="checkbox" className="mr-2" />
              $500+
            </label>
          </div>
        </div>

        {/* Rating Filter */}
        <div className="mb-4">
          <button className="w-full text-left p-2 border-b">Rating</button>
          <div className="p-6">
            <label className="block">
              <input type="checkbox" className="mr-2" />
              4 Stars & Up
            </label>
            <label className="block">
              <input type="checkbox" className="mr-2" />
              3 Stars & Up
            </label>
          </div>
        </div>

        {/* Clear Filters Button */}
        <div className="text-center mt-4">
          <button className="px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600">
            Clear Filters
          </button>
        </div>
      </div>

      {/* Right Side: Products */}
      <div className="w-3/4 pr-8">
        <h2 className="text-2xl font-semibold mb-6">All Products</h2>
        <div className="product-grid grid grid-cols-1 gap-6">
          {products.map((product) => (
            <>
            
            <ProductCard key={product._id} product={product} />
            </>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Products;
