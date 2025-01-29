import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../api/api";

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const { data } = await axios.get(`/products/${id}`);
        setProduct(data);
      } catch (error) {
        console.error("Error fetching product", error);
      }
    };

    fetchProduct();
  }, [id]);

  if (!product) return <p>Loading...</p>;

  return (
    <div>
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <p>{product.specification}</p>
      <p>Rating: {product.rating}</p>
      <p>Reviews: {product.reviews}</p>
      <button>Add to Cart</button>
    </div>
  );
};

export default ProductDetail;
